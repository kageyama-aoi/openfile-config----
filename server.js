const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const app = express();
const configPath = './config.json';

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // publicディレクトリを静的ファイルのルートとして設定

// 設定の取得
app.get('/config', (req, res) => {
  fs.readFile(configPath, 'utf8', (err, data) => {
    if (err) return res.status(500).send('設定ファイルの読み込みに失敗しました。');
    res.send(JSON.parse(data));
  });
});

// 設定の保存
app.post('/config', (req, res) => {
  fs.writeFile(configPath, JSON.stringify(req.body, null, 2), 'utf8', (err) => {
    if (err) return res.status(500).send('設定ファイルの保存に失敗しました。');
    res.send({ message: '設定が保存されました。' });
  });
});

// Pythonスクリプトを呼び出してファイルパスを取得するエンドポイント
app.get('/get-file-path', (req, res) => {
  console.time('pythonScriptExecution'); // 計測開始
  const pythonProcess = spawn('python', ['./scripts/get_file_path.py']);
  let filePath = '';
  let errorData = '';

  pythonProcess.stdout.on('data', (data) => {
    // Pythonからの出力がUTF-8であることを期待してtoString()で処理
    filePath += data.toString().trim();
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
    errorData += data.toString();
  });
  
  // Pythonスクリプトの標準出力エンコーディングをUTF-8として扱う
  pythonProcess.stdout.setEncoding('utf8');

  pythonProcess.on('close', (code) => {
    console.timeEnd('pythonScriptExecution'); // 計測終了して時間を表示
    if (code !== 0) {
      console.error(`Python script exited with code ${code}. Stderr: ${errorData}`);
      return res.status(500).json({ error: 'ファイルパスの取得に失敗しました (Pythonスクリプトエラー)。', details: errorData });
    }
    res.json({ filePath: filePath });
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python subprocess.', err);
    res.status(500).json({ error: 'ファイルパスの取得に失敗しました (Pythonプロセス起動エラー)。' });
  });
});


app.listen(3000, () => {
  console.log('サーバーがポート3000で起動しました。');
});
