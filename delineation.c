#include "ift.h"

/* Author: Alexandre Xavier Falcão (September 10th, 2023)

   Description: Delineates objects (e.g., parasite eggs) from the
   decoded saliency maps.

*/

/* Complete the code below to delineate objects using Dynamic
   Trees. Use Equation 16 from articles/2019_IFT_DGCI.pdf */

iftImage *DynamicTrees(iftImage *orig, iftImage *seeds_in, iftImage *seeds_out)
{
  iftMImage *mimg = iftImageToMImage(orig, LAB_CSPACE);
  iftImage *pathval = NULL, *label = NULL, *root = NULL;
  iftGQueue *queue = NULL;
  int i, p, neighbor_index, tmp;
  iftVoxel u, v;
  iftLabeledSet *seeds = seeds_in;
  iftAdjRel *adjacency = iftCircular(1.0);
  // TODO: create C(p) that accumulate the color
  // TODO: create N(p) that does something(???)

  // Initialization

  pathval = iftCreateImage(mimg->xsize, mimg->ysize, mimg->zsize);
  label = iftCreateImage(mimg->xsize, mimg->ysize, mimg->zsize);
  root = MImageGradient(mimg, adjacency);
  queue = iftCreateGQueue(4095 + 1, mimg->n, pathval->val);

  /* Initialize costs */

  while (seeds != NULL)
  {
    p = seeds->elem;
    label->val[p] = seeds->label;
    pathval->val[p] = 0;
    iftInsertGQueue(&queue, p);
    seeds = seeds->next;
  }

  for (p = 0; p < mimg->n; p++)
  {
    if (queue->L.elem[p].color == IFT_WHITE)
    { /* it is not seed */
      pathval->val[p] = IFT_INFINITY_INT;
      iftInsertGQueue(&queue, p);
    }
  }

  /* Propagate Optimum Paths by the Image Foresting Transform */

  while (!iftEmptyGQueue(queue))
  {
    p = iftRemoveGQueue(queue);
    u = iftGetVoxelCoord(root, p);

    for (i = 1; i < adjacency->n; i++)
    {
      v = iftGetAdjacentVoxel(adjacency, u, i);

      if (iftValidVoxel(root, v))
      {
        neighbor_index = iftGetVoxelIndex(root, v);

        if (queue->L.elem[neighbor_index].color != IFT_BLACK)
        {

          // TODO: modification here so that root->val[neighbor_index] is C(p)/N(p)
          tmp = iftMax(pathval->val[p], root->val[neighbor_index]);

          if (tmp < pathval->val[neighbor_index])
          {
            iftRemoveGQueueElem(queue, neighbor_index);
            label->val[neighbor_index] = label->val[p];

            pathval->val[neighbor_index] = tmp;
            iftInsertGQueue(&queue, neighbor_index);
            // TODO: Update C(p) and N(p) here (?)
          }
        }
      }
    }
  }

  iftDestroyAdjRel(&adjacency);
  iftDestroyGQueue(&queue);
  iftDestroyImage(&root);
  iftDestroyImage(&pathval);

  return (label);
}

iftImage *ImageGradient(iftImage *img, iftAdjRel *A)
{
  iftImage *gradI = iftCreateImage(img->xsize, img->ysize, img->zsize);
  float *mag = iftAllocFloatArray(A->n);
  float *gx = iftAllocFloatArray(3);
  float *gy = iftAllocFloatArray(3);
  float *gz = iftAllocFloatArray(3);

  for (int i = 0; i < A->n; i++)
    mag[i] = sqrt(A->dx[i] * A->dx[i] + A->dy[i] * A->dy[i] + A->dz[i] * A->dz[i]);

  for (ulong p = 0; p < img->n; p++)
  {
    iftVoxel u = iftGetVoxelCoord(img, p);

    for (int b = 0; b < 3; b++)
    {
      gx[b] = 0;
      gy[b] = 0;
      gz[b] = 0;
    }

    for (int i = 1; i < A->n; i++)
    {
      iftVoxel v = iftGetAdjacentVoxel(A, u, i);
      if (iftValidVoxel(img, v))
      {
        int q = iftGetVoxelIndex(img, v);
        for (int b = 0; b < 3; b++)
        {
          gx[b] += ((float)img->val[q] - (float)img->val[p]) * A->dx[i] / mag[i];
          gy[b] += ((float)img->Cb[q] - (float)img->Cb[p]) * A->dy[i] / mag[i];
          gz[b] += ((float)img->Cr[q] - (float)img->Cr[p]) * A->dz[i] / mag[i];
        }
      }
    }
    float Gx = 0.0, Gy = 0.0, Gz = 0.0;
    for (int b = 0; b < 3; b++)
    {
      gx[b] = gx[b] / (A->n - 1);
      gy[b] = gy[b] / (A->n - 1);
      gz[b] = gz[b] / (A->n - 1);
      Gx += gx[b];
      Gy += gy[b];
      Gz += gz[b];
    }
    Gx /= 3;
    Gy /= 3;
    Gz /= 3;
    gradI->val[p] = iftRound(sqrtf(Gx * Gx + Gy * Gy + Gz * Gz));
  }

  iftFree(mag);
  iftFree(gx);
  iftFree(gy);
  iftFree(gz);

  return (gradI);
}

iftImage *Watershed(iftImage *gradI, iftImage *seeds_in, iftImage *seeds_out)
{
  iftImage *pathval = NULL, *label = NULL;
  iftGQueue *Q = NULL;
  int i, p, q, tmp;
  iftVoxel u, v;
  iftAdjRel *A = iftCircular(1.0);

  // Initialization

  pathval = iftCreateImage(gradI->xsize, gradI->ysize, gradI->zsize);
  label = iftCreateImage(gradI->xsize, gradI->ysize, gradI->zsize);
  Q = iftCreateGQueue(iftMaximumValue(gradI) + 1, gradI->n, pathval->val);

  /* Initialize costs */

  for (p = 0; p < gradI->n; p++)
  {
    pathval->val[p] = IFT_INFINITY_INT;
    if (seeds_in->val[p] != 0)
    {
      label->val[p] = seeds_in->val[p];
      pathval->val[p] = 0;
    }
    else
    {
      if (seeds_out->val[p] != 0)
      {
        label->val[p] = 0;
        pathval->val[p] = 0;
      }
    }
    iftInsertGQueue(&Q, p);
  }

  /* Propagate Optimum Paths by the Image Foresting Transform */

  while (!iftEmptyGQueue(Q))
  {
    p = iftRemoveGQueue(Q);
    u = iftGetVoxelCoord(gradI, p);

    for (i = 1; i < A->n; i++)
    {
      v = iftGetAdjacentVoxel(A, u, i);

      if (iftValidVoxel(gradI, v))
      {
        q = iftGetVoxelIndex(gradI, v);

        if (Q->L.elem[q].color != IFT_BLACK)
        {

          tmp = iftMax(pathval->val[p], gradI->val[q]);

          if (tmp < pathval->val[q])
          {
            iftRemoveGQueueElem(Q, q);
            label->val[q] = label->val[p];

            pathval->val[q] = tmp;
            iftInsertGQueue(&Q, q);
          }
        }
      }
    }
  }

  iftDestroyAdjRel(&A);
  iftDestroyGQueue(&Q);
  iftDestroyImage(&pathval);

  return (label);
}

int main(int argc, char *argv[])
{

  /* Example: delineation salie 1 objs */

  if (argc != 4)
  {
    iftError("Usage: delineation <P1> <P2> <P3>\n"
             "[1] folder with the salience maps\n"
             "[2] layer (1,2,...) to create the results\n"
             "[3] output folder with the resulting images\n",
             "main");
  }

  timer *tstart = iftTic();

  char *filename = iftAllocCharArray(512);
  int layer = atoi(argv[2]);
  char suffix[12];
  sprintf(suffix, "_layer%d.png", layer);
  iftFileSet *fs = iftLoadFileSetFromDirBySuffix(argv[1], suffix, true);
  char *output_dir = argv[3];
  iftMakeDir(output_dir);
  iftColorTable *ctb = iftCreateRandomColorTable(10);
  iftAdjRel *A = iftCircular(3.0);
  iftAdjRel *B = iftCircular(1.5);
  iftAdjRel *C = iftCircular(1.0);

  for (int i = 0; i < fs->n; i++)
  {
    printf("Processing image %d of %ld\r", i + 1, fs->n);
    char *basename1 = iftFilename(fs->files[i]->path, suffix);
    char *basename2 = iftFilename(fs->files[i]->path, ".png");
    iftImage *salie = iftReadImageByExt(fs->files[i]->path);
    sprintf(filename, "./images/%s.png", basename1);
    iftImage *orig = iftReadImageByExt(filename);

    /* Delineate parasite */

    iftImage *gradI = ImageGradient(orig, A);
    iftImage *bin = iftThreshold(salie, iftOtsu(salie), IFT_INFINITY_INT, 255);
    iftImage *seeds_in = iftSelectCompInAreaInterval(bin, NULL, 400, 4000);
    iftDestroyImage(&bin);
    iftImage *img = NULL;

    if (iftMaximumValue(seeds_in) == 0)
      img = iftCopyImage(orig);
    else
    {
      iftSet *S = NULL;
      bin = iftDilateBin(seeds_in, &S, 15.0);
      iftDestroySet(&S);
      iftImage *seeds_out = iftComplement(bin);
      iftDestroyImage(&bin);
      bin = iftFastLabelComp(seeds_in, NULL);
      iftDestroyImage(&seeds_in);
      seeds_in = bin;

      /* iftImage *label = Watershed(gradI,seeds_in,seeds_out); */
      iftImage *label = DynamicTrees(orig, seeds_in, seeds_out);
      iftFImage *weight = iftSmoothWeightImage(gradI, 0.5);
      iftImage *smooth_label = iftFastSmoothObjects(label, weight, 5);
      iftDestroyImage(&label);
      label = smooth_label;
      iftDestroyFImage(&weight);
      img = iftCopyImage(orig);
      iftDrawBorders(img, label, C, ctb->color[1], B);
      iftDestroyImage(&label);
      iftDestroyImage(&seeds_out);
    }

    iftDestroyImage(&seeds_in);
    iftDestroyImage(&salie);
    iftDestroyImage(&orig);
    iftDestroyImage(&gradI);

    /* save resulting image */

    sprintf(filename, "%s/%s.png", output_dir, basename2);
    iftWriteImageByExt(img, filename);

    iftDestroyImage(&img);
    iftFree(basename1);
    iftFree(basename2);
  }

  iftDestroyColorTable(&ctb);
  iftFree(filename);
  iftDestroyFileSet(&fs);
  iftDestroyAdjRel(&A);
  iftDestroyAdjRel(&B);
  iftDestroyAdjRel(&C);

  printf("\nDone ... %s\n", iftFormattedTime(iftCompTime(tstart, iftToc())));

  return (0);
}
