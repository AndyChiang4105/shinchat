# 環境設定
以下為可順利運行環境，其他版本沒試過，還沒安裝環境的建議使用虛擬環境，如 [Anaconda](https://www.anaconda.com/download) 安裝
  - 安裝完先在 Anaconda Navigator 設定一個虛擬環境
  - 設定完後搜尋 Anaconda Prompt，右鍵以系統管理員身份執行
  - 使用以下指令切換環境 `activate YOUR_ENV_NAME`
---
## 1.安裝環境
1. 安裝 [python 3.10.11](https://www.python.org/downloads/release/python-31011/) 版本 
    - 使用虛擬環境的可以執行 `conda install python=3.10.11` 
2. 控制台輸入 `nvidia-smi` 查看CUDA版本
    - CUDA 版本必須 >= **12.1** ，小於的話去 nvidia experience 更新驅動
3. 安裝 [CUDA Toolkit 12.1](https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local)，選擇對應的版本，Installer Type 要選 `exe(local)`
4. 安裝 pytorch，此指令對應到 CUDA Toolkit 12.1 版，其他版本沒試過建議不要亂改，其他版本可以在[這裡](https://pytorch.org/get-started/previous-versions/)找到
```bash
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
```
5.執行以下程式確認是否可以正常使用以及版本號
```python
import torch
print("Is CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
import torchvision
print("TorchVision version:", torchvision.__version__)
```
印出結果應該要類似這樣，TorchVision version 如果沒有出現 +cu121 代表有問題
```
Is CUDA available: True
CUDA version: 12.1
TorchVision version: 0.16.2+cu121
```
6. 下載 [Visual Studio 2022](https://visualstudio.microsoft.com/zh-hant/)，打開後選擇「**使用 C++的桌面開發**」這個工具包下載 (這步不確定是不是必須)
7. 下載 [ffmpeg](https://www.gyan.dev/ffmpeg/builds/#release-builds)，選擇 `ffmpeg-release-full.7z` 下載
    - 詳細教學看[這篇](https://vocus.cc/article/64701a2cfd897800014daed0)，要設定環境變數

 ## 2.下載專案必要檔案
 1. 執行以下命令下載專案
```bash
 git clone https://github.com/AndyChiang4105/shinchat.git
```
 4. 在 shinchat 資料夾下開啟 cmd，執行以下命令安裝套件 (可能要等蠻久的)
```bash
pip install -r requirements.txt
```
3. 下載 [**卡芙卡**](https://soochowmss-my.sharepoint.com/personal/10156215_mss_scu_edu_tw/_layouts/15/onedrive.aspx?id=%2Fpersonal%2F10156215%5Fmss%5Fscu%5Fedu%5Ftw%2FDocuments%2F%E8%A0%9F%E7%AD%86%E5%B0%8F%E6%96%B0&ga=1) 資料夾下的 `pretrained_models` 以及其他兩個 tts 模型
4. 將剛剛下載的 `pretrained_models` 替換掉這個資料夾 `shinchat\GPT_SoVITS\pretrained_models`
5. 將 `.cpkt` 模型放到 `shinchat\GPT_weights` 資料夾下
6. 將 `.pth` 模型放到 `shinchat\SoVITS_weights` 資料夾下
7. 去這裡申請一組免費的 [OpenAI API key](https://github.com/chatanywhere/GPT_API_free)，並在「系統變數」中新增
```bash
setx OPENAI_API_KEY <your-api-key>
```
8. 在 cmd 中輸入 `echo %OPENAI_API_KEY%` 確認有設定成功

## 3.執行專案
到這邊環境應該已經完全設定好了，接著即可執行檔案
1. 在 vscode 中用「開啟資料夾」的方式打開 shinchat 資料夾
    - 使用 Anaconda 的話要先在 Vscode 右下角的 Interpreter (顯示python版本的那個地方) 切換到虛擬環境
2. 先使用指令 `python api.py` 開啟 api server
3. 新增一個終端機來執行 `python app.py` 開啟網站  
初次執行時要先下載 `faster_whisper` 的模型，因為是在本地執行

# 使用LangSmith
1. 下載套件
```bash
pip install -U langsmith
```
2. 到[這裡](https://smith.langchain.com/settings)申請 LangSmith 的 API key
3. 在 cmd 輸入指令設定兩組環境變數
```bash
setx LANGCHAIN_TRACING_V2 true
```
```bash
setx LANGCHAIN_API_KEY <your-api-key>
```
4. 在 [LangSmith](https://smith.langchain.com/) 中的 Projects 下即可看到每次使用 langchain 的詳細訊息
5. 角色模板連結 : [shin_prompt](https://smith.langchain.com/hub/shinchat/shin_prompt)

#百度情感分析
1.到[這裡](https://ai.baidu.com/tech/nlp_apply/sentiment_classify)申請接口的client_id，client_secret

2.將得到的client_id，client_secret輸入到gettoken.py，獲得access_token

3.將access_token輸入emotion.py執行

4.請求格式{
          "text": "今天天氣真好"
          }
          
5.得到回應參數![image](https://github.com/AndyChiang4105/shinchat/assets/147487437/0f7451fc-7962-4203-8398-b41cf5413e70)

# 代辦事項
- 前端
  - [ ] 製作使用者介面
  - [ ] 加入網頁字幕顯示功能
  - [ ] 實現角色動畫撥放
- 後端
  - [ ] 連接情感分析與角色動畫
  - [ ] 實現 GPT 記憶功能
  - [ ] 連接向量資料庫
- 其他
  - [ ] 進行 VITS 模型訓練
  - [ ] 製作角色動畫
  - [ ] 準備向量資料庫文本
