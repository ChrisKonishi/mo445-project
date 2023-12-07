Sempre utilizando a segunda camada
Começar com 1 kernel por marcador

1 marcador de fundo e 1 de obj por imagem

Aumentar número de kernel
Desequilibrar número de marcadores



1 per marker 1 img (1)
Average IoU seg: 0.314976617787574
Average Dice seg: 0.3186196139452118
Average IoU bb: 0.31337832406848476
Diversas imagens vazias

1 per marker 2 img (1, 2)
Average IoU seg: 0.41322708283455206
Average Dice seg: 0.4242076117573453
Average IoU bb: 0.41094884205758503

1 per marker 3 img (1, 2, 3)
Average IoU seg: 0.4591886824517619
Average Dice seg: 0.4750771957482139
Average IoU bb: 0.45417419380414326
Começam a surgir artefatos no topo na imagem

1 per marker 3 img (1, 2, 3, 4)
Average IoU seg: 0.22331956349451917
Average Dice seg: 0.23010805866368747
Average IoU bb: 0.220850244524312
Os artefatos pioram, apresentar esses dados

3 per marker 3 imgs
Average IoU seg: 0.6555793660342035
Average Dice seg: 0.6855735460556588
Average IoU bb: 0.6433182215671766

5 per marker 3 imgs
Average IoU seg: 0.6738912122205223
Average Dice seg: 0.7114557434468557
Average IoU bb: 0.6719334900530577

7 per marker 3 imgs
Average IoU seg: 0.6643655507770138
Average Dice seg: 0.7048131847715485
Average IoU bb: 0.65296431729503

5 per marker 4 imgs
Average IoU seg: 0.5221304353376219
Average Dice seg: 0.5484856443460463
Average IoU bb: 0.5138566376203902
Aumento de kernes reduz os artefatos, mas não trouxe melhoria


Observação sensível a escolha de imagens



-> aumentando imagens, reduz a quantidade de saliencias vazias
