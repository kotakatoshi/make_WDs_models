#!/bin/bash

# Macc の値のリストを定義
Macc_list=(0.01 0.03 0.05 0.1 0.15 0.2)

# Macc リスト内の各値に対してループを実行
for Macc in "${Macc_list[@]}"
do
  # max_age を整数として計算
  max_age=$(echo "scale=0; $Macc / 1e-5" | bc)

  # save_model_filename を accreted_xxx.mod の形式にフォーマット
  formatted_macc=$(printf "%03d" $(echo "$Macc * 100" | bc | awk '{print int($1)}'))
  save_model_filename="accreted_${formatted_macc}.mod"

  # shmesa コマンドを実行
  echo "Running for Macc=$Macc"
  shmesa change inlist_wd_acc_small_dm max_age "$max_age"
  shmesa change inlist_wd_acc_small_dm save_model_filename "'$save_model_filename'"

  # rn コマンドを実行
  ./rn
done
