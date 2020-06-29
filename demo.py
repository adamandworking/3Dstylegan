import os

os.system('python run_generator.py generate-images --network=gdrive:networks/stylegan2-ffhq-config-f.pkl --seeds=6600-6625 --truncation-psi=0.5 --mode=2D')

os.system('python run_generator.py generate-images --network=pkl_folder/Hilbert_stripe.pkl --seeds=0-500 --truncation-psi=0.5 --mode=Hilbert')
os.system('python run_generator.py truncation-trick --network=pkl_folder/Hilbert_stripe.pkl --seeds=270 --interval=0.1 --mode=Hilbert')
os.system('python run_generator.py style-mixing-example --network=pkl_folder/Hilbert_stripe.pkl --row-seeds=270,147 --col-seeds=68,79,75,71,166 --truncation-psi=1.0 --col-styles=1,2,3,4 --mode=Hilbert')

