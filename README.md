# check-image
OSSツール使用手順

I.環境設定
■ンストール機能手順
	１．PCにPythonをインストールする(バージョン3.9.10の６４bit）					
	２．Pip追加					
	３．Cmdで以下のステートメントでscikit-image追加する					
		pip install --upgrade scikit-image				
	４．Imutils追加					
		pip install --upgrade imutils
	５．numpyを追加
		pip install numpy			
	６．imageを追加
		pip install Image
	７．Opencvライブラリー追加					
		pip install --upgrade opencv-python
			
II．OSSツールの注意

※注意点
・OssツールはPCのcommandで動いています。
・投入画像のフォーマットはjpgまたはpngです。それ以外はダメです。
・実行する方法では２つのモードがあって、ファイルモードとフォルダモードになります。
・実行モードを選択するのはNectoolのFileボタンから、選んでください。
・フォルダモードに関して、・フォルダモード実行する前にexpectフォルダとrealフォルダに存在している画像のが必要で、
または比較したい画像の名前が一致しなといけないので、必ず注意してください。


-----------------------------------------------------------------------------------
[English version]
-----------------------------------------------------------------------------------

OSS tool usage procedure

I. Preferences
■ Stall function procedure
1. 1. Install Python on your PC (version 3.9.10 with 64bit)
2. 2. Add Pip
3. 3. Add scikit-image with the following statement in Cmd
pip install --upgrade scikit-image
4. Added Imutils
pip install --upgrade imutils
5. Add numpy
pip install numpy
6. Add Image
pip install Image
7. Opencv library added
pip install --upgrade opencv-python
.
II. OSS tool notes

※important point
-The Oss tool runs on the command of the PC.
-The format of the input image accept only jpg or png
-There are two modes to execute, file mode and folder mode.
-Select the execution mode from the File button of Nectool.

II. Run tool OSS
- Run with layout tool:
	1. Choose to folder contain tool OSS => Open window cmd => Typing: python main.py => Then popup tool OSS open
	2. Choose mode run tool (Run compare two file / run compare two folder / Exit to close tool)
	3. Choose file or folder to compare based on mode run above.
	4. Click start to compare.
- Run with command line:
	1. Choose to folder contain tool OSS => Open window cmd => Typing: python folder.py expect="path folder expect" real="path folder real" result="path folder result"
	2. Click button Enter in keybroad then start compare.


