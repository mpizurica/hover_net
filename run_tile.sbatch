#!/usr/bin/bash
#SBATCH --job-name=run_tile
#SBATCH --output=run_tile.%j.out
#SBATCH --error=run_tile.%j.err
#SBATCH --time=48:00:00
#SBATCH -p gpu
#SBATCH -G 1
#SBATCH --cpus-per-gpu=10

ml load python/3.9.0
ml load biology
ml load openslide/3.4.1
ml load opencv/4.5.5
ml load gcc/9.1.0

source /oak/stanford/groups/ogevaert/code/hover_net/hover/bin/activate

python3.9 run_infer.py \
            --gpu='0' \
            --nr_types=6 \
            --type_info_path=type_info.json \
            --batch_size=32 \
            --model_mode=fast \
            --model_path=hovernet_fast_pannuke_type_tf2pytorch.tar \
            --nr_inference_workers=8 \
            --nr_post_proc_workers=16 \
            tile \
            --input_dir=/oak/stanford/groups/ogevaert/data/Patho-RNA-GAN/src/elucinated_images128_53k_1000/ \
            --output_dir=/oak/stanford/groups/ogevaert/data/Patho-RNA-GAN/hover_net/synthetic/ \
            --mem_usage=0.1 
