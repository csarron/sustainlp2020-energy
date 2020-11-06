
for m in bert-base distilbert mobilebert roberta-base; do
source "data/env/${m}.env"
CUDA_VISIBLE_DEVICES="0" python run_energy_squad.py \
        --model_type ${model_type} \
        --model_name_or_path ${model_name_or_path} \
        --do_eval ${lower_case_arg} \
        --predict_file dev-v1.1.1000.json \
        --per_gpu_eval_batch_size=32 \
        --max_seq_length 320 \
        --doc_stride 128 \
        --data_dir data \
        --output_dir data/${m} 2>&1 | tee data/eval-${m}-dev-1k.log
done

for m in roberta-base bert-base distilbert mobilebert; do
  source "data/env/${m}.env"
  for b in 1 $(seq 2 2 32); do
    log_dir=data/${model}-squad-v1/dev1k/b-${b}
    mkdir -p "${log_dir}"
    for i in `seq 1 1 10`; do
      echo $i
      python -c "import datetime;now=datetime.datetime.now();timestamp='{}-{}-{}-{}-{}-{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second);print(timestamp)" > ${log_dir}/t$i-start.txt
      CUDA_VISIBLE_DEVICES="0" python run_energy_squad.py \
        --model_type ${model_type} \
        --model_name_or_path ${model_name_or_path} \
        --do_eval ${lower_case_arg} \
        --predict_file dev-v1.1.1000.json \
        --per_gpu_eval_batch_size=$b \
        --max_seq_length 320 \
        --doc_stride 128 \
        --log_energy_consumption \
        --energy_output_dir ${log_dir}/t$i \
        --data_dir data \
        --output_dir ${log_dir} 2>&1 | tee ${log_dir}/eval-energy-t$i.log
      python -c "import datetime;now=datetime.datetime.now();timestamp='{}-{}-{}-{}-{}-{}'.format(now.year,now.month,now.day,now.hour,now.minute,now.second);print(timestamp)" > ${log_dir}/t$i-end.txt
      sleep 3
    done
  done 
done

for m in roberta-base bert-base distilbert mobilebert; do
  source "data/env/${m}.env"
  echo '' > ${m}-eip.log
  for b in 1 $(seq 2 2 32); do
  python compute_efficiency_info.py data/${model}-squad-v1/dev1k/b-${b} >> ${m}-eip.log
  done
done 

for m in roberta-base bert-base distilbert mobilebert; do
  source "data/env/${m}.env"
  echo '' > ${m}-wattsup.log
  for b in 1 $(seq 2 2 32); do
  python compute_wattsup_energy.py data/4-models-10-runs-dev1k.txt -d data/${model}-squad-v1/dev1k/b-${b} -p t -i 10 >> ${m}-wattsup.log
  done
done 

echo '' > bert-base-wattsup.log
for b in 1 $(seq 2 2 32); do
python compute_wattsup_energy.py data/four-models-10-runs.txt -d data/bert-base-uncased-squad-v1/new/b-$b/ -p t -i 10 >> bert-base-wattsup.log
done 

# generate inference duration logs
grep -r 'Evaluation done in total ' roberta-base-squad-v1/dev1k/b-*/*.log > roberta-base-latency.txt
grep -r 'Running evaluation ' roberta-base-squad-v1/dev1k/b-*/*.log > roberta-start.txt

# extract inference start and end from logs
python extract_duration.py data/energy-10-runs-log/distilbert-start.txt -o data/energy-10-runs-log/distilbert
python extract_duration.py data/energy-10-runs-log/distilbert-latency.txt -o data/energy-10-runs-log/distilbert -e


for m in roberta-base bert-base distilbert mobilebert; do
  echo '' > data/energy-10-runs-log/${m}-inference-wattsup.log
  for b in 1 $(seq 2 2 32); do
  python compute_wattsup_energy.py data/4-models-10-runs-dev1k.txt -d data/energy-10-runs-log/${m}/b-${b} -p t -i 10 >> data/energy-10-runs-log/${m}-inference-wattsup.log
  done
done