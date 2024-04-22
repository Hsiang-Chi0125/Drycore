# Run Drycore
- **IdealizedSpectralGCM.jl**

  Source code & experiment : 
```
$ ls /work/home/YCL.pamip_data/IdealizedSpectralGCM.jl
  exp(跟執行有關) src(Source code)
```
- **environment.yml**

  跟環境有關

  HSt42 : 42 (64x128), 21 (32x64)

  - Run_HS.jl : 執行檔

  - HS.jl : model 大目錄

```
$ vi /work/home/YCL.pamip_data/IdealizedSpectralGCM.jl/exp/HSt42/Run_HS.jl

using JGCM #使用的模式
  
include("HS.jl") 

#############################################################
end_day = 1200 #要跑幾天
spinup_day = 200 #前面不要的天數, 最終天數為end_day-spinup_day

#end_day = 2 
#spinup_day = 1

physics_params = Dict{String,Float64}("σ_b"=>0.7, "k_f" => 1.0, "k_a" => 1.0/40.0, "k_s" => 1.0/4.0, "ΔT_y" => 60.0, "Δθ_z" => 10.0)  #跟forcing有關的參數, ΔT_y跟平衡溫度有關
op_man = Atmos_Spectral_Dynamics_Main(physics_params, end_day, spinup_day)  #餵進JGCM
Finalize_Output!(op_man, "HS_OpM.dat", "HS_mean.dat")  #Output, HS_OpM.dat為二進位檔, 要自己寫成nc檔。HS_mean.dat為時間平均檔
Sigma_Zonal_Mean_Contourf(op_man, "Contourf")  #自動畫圖, 會存在Contourf_Teq.png  Contourf_T.png  Contourf_U.png  Contourf_V.png中
```

nd : 高度層數

nθ : 

nλ : 
## 實驗改參數
```
$ vi /work/home/YCL.pamip_data/IdealizedSpectralGCM.jl/src/Atmos_Param/HS_Forcing.jl
```
**方法一**
要調Teq的矩陣
```
  for  k = 1:nd
    grid_p_norm .= grid_p_full[:,:,k]/p_ref  #.的意思是有附值，原本的值不會動到

    grid_t_eq[:,:,k] .= (t_zero .- ΔT_y*sinθ2_2d  .- Δθ_z*cosθ2_2d.*log.(grid_p_norm)) .*  grid_p_norm.^kappa
    grid_t_eq[:,:,k] .= max.( t_strat, grid_t_eq[:,:,k])
  end
```
**方法二**
在公式後面多加tern
```
  for k=1:nd
    σ .= grid_p_full[:,:,k]./grid_ps

    #todo
    @assert(maximum(σ .- σ_b)/(1.0 - σ_b) <= 1.0)

    k_t .= k_a .+ (k_s - k_a)/(1.0-σ_b) * max.(0.0, σ .- σ_b) .* cosθ4_2d

    grid_δt[:,:,k] .-= k_t .* (grid_t[:,:,k] - grid_t_eq[:,:,k]) .+ 2  #看+2要在哪

  end
```
## Run
需要先改julia, precompiled JGCM
(如果只改Run_HS.jl就不用)
```
$ julia
julia>
```
打右中括號
```
pkg> activate /work/home/YCL.pamip_data/IdealizedSpectralGCM.jl
```
按Backspace
```
julia> using JGCM
julia> exit()
```
才能執行實驗
```
$ nohup julia Run_HS.jl &
```
