python run_infer.py \
--gpu='0' \
--nr_types=6 \
--type_info_path=type_info.json \
--batch_size=64 \
--model_mode=fast \
--model_path=../pretrained/hovernet_fast_pannuke_type_tf2pytorch.tar \
--nr_inference_workers=8 \
--nr_post_proc_workers=16 \
tile \
--input_dir=/home/users/mpizuric/code/WSI_mutation/code/img_name_to_index.csv \
--output_dir=/oak/stanford/groups/ogevaert/data/Prad-TCGA/hover_net/ \
--mem_usage=0.1 \
--draw_dot \
--save_qupath
