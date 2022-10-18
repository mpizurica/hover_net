#!/usr/bin/bash
#SBATCH --job-name=run_wsi24GB
#SBATCH --output=run_wsi24GB.%j.out
#SBATCH --error=run_wsi24GB.%j.err
#SBATCH --time=48:00:00
#SBATCH -p gpu
#SBATCH -G 1
#SBATCH -C GPU_MEM:24GB
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
        --batch_size=64 \
        --model_mode=fast \
        --model_path=hovernet_fast_pannuke_type_tf2pytorch.tar \
        --nr_inference_workers=8 \
        --nr_post_proc_workers=16 \
        wsi \
        --input_dir=/oak/stanford/groups/ogevaert/data/Roche-TCGA/TCGA-PRAD/ \
        --output_dir=/oak/stanford/groups/ogevaert/data/Prad-TCGA/hover_net/ \
        --input_mask_dir=/oak/stanford/groups/ogevaert/data/Prad-TCGA/masks_TCGA/ \
        --cache_path=/oak/stanford/groups/ogevaert/data/Prad-TCGA/cache/ \
        --save_thumb \
        --save_mask
