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
--output_dir=dataset/sample_wsis/out/ \
--input_mask_dir=/oak/stanford/groups/ogevaert/data/Prad-TCGA/masks_TCGA/ \
--save_thumb \
--save_mask
