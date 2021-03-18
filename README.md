# Image-Compressor

## Alessandro Capelli

### Introduzione
Questo progetto riguarda lo sviluppo e utilizzo della DCT2 in ambiente open source. Come ambiente di sviluppo è stato scelto Python, per consentire di sfruttare la velocità, la dinamicità sintattica e semantica del linguaggio (interpretato) e la sua caratteristica di essere cross-platform. Il progetto è suddiviso in due fasi:
- inizialmente è stata sviluppata una libreria "homemade" (chiamata "DCT2_homemade") che implementa una versione non ottimizzata di DCT2 (e DCT) normalizzata, che è stata confrontata con una libreria ottimizzata (chiamata "sci-py.fft") che implementa la versione fast (FFT) della DCT2 (anch’essa normalizzata).
- successivamente è stato sviluppato un software (chiamato "imageCompressor.py") che implementa un semplice algoritmo di compressione delle immagini in toni di grigio, in particolare, per immagini in formato BMP.
