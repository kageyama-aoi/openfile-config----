const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

const app = express();

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public'))); // publicディレクトリを静的ファイルのルートとして設定

// --- Helper Functions for Config File Operations ---

// Helper function to read a config file
function readConfigFile(filePath, res) {
  // セキュリティ: パストラバーサルを防ぎ、.jsonファイルのみを許可
  // このチェックは呼び出し元で行うか、ファイル名が固定の場合は不要
  const baseFilename = path.basename(filePath);
  if (baseFilename.includes('..') || !baseFilename.endsWith('.json')) {
    return res.status(400).send('無効なファイル名、または許可されていないファイル形式です。');
  }

  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      if (err.code === 'ENOENT') {
        return res.status(404).send('設定ファイルが見つかりません。');
      }
      console.error(`設定ファイル "${filePath}" の読み込みに失敗しました:`, err);
      return res.status(500).send('設定ファイルの読み込みに失敗しました。');
    }
    try {
      const jsonData = JSON.parse(data);
      res.send(jsonData);
    } catch (parseError) {
      console.error(`設定ファイル "${filePath}" のJSON解析に失敗しました:`, parseError);
      return res.status(500).send('設定ファイルの形式が正しくありません。');
    }
  });
}

// Helper function to write a config file
function writeConfigFile(filePath, data, res) {
  // セキュリティ: パストラバーサルを防ぎ、.jsonファイルのみを許可
  const baseFilename = path.basename(filePath);
  if (baseFilename.includes('..') || !baseFilename.endsWith('.json')) {
    return res.status(400).send('無効なファイル名、または許可されていないファイル形式です。');
  }

  fs.writeFile(filePath, JSON.stringify(data, null, 2), 'utf8', (err) => {
    if (err) {
      console.error(`設定ファイル "${filePath}" の保存に失敗しました:`, err);
      return res.status(500).send('設定ファイルの保存に失敗しました。');
    }
    res.send({ message: '設定が保存されました。' });
  });
}

// --- API Endpoints ---

// 設定ファイルの取得 (動的ファイル名対応)
app.get('/api/configs/:filename', (req, res) => {
  const { filename } = req.params;
  // API経由の場合は、ファイル名がパスを含まないことを確認
  if (path.basename(filename) !== filename) {
    return res.status(400).send('無効なファイル名形式です。ファイル名のみを指定してください。');
  }
  const filePath = path.join(__dirname, filename);
  readConfigFile(filePath, res);
});

// 設定ファイルの保存 (動的ファイル名対応)
app.post('/api/configs/:filename', (req, res) => {
  const { filename } = req.params;
  // API経由の場合は、ファイル名がパスを含まないことを確認
  if (path.basename(filename) !== filename) {
    return res.status(400).send('無効なファイル名形式です。ファイル名のみを指定してください。');
  }
  const filePath = path.join(__dirname, filename);
  writeConfigFile(filePath, req.body, res);
});

// --- Legacy Endpoints for config.json (Backward Compatibility) ---
const defaultConfigPath = path.join(__dirname, 'config.json');
app.get('/config', (req, res) => readConfigFile(defaultConfigPath, res));
app.post('/config', (req, res) => writeConfigFile(defaultConfigPath, req.body, res));

// Pythonスクリプトを呼び出してファイルパスを取得するエンドポイント
app.get('/get-file-path', (req, res) => {
  console.time('pythonScriptExecution'); // 計測開始
  const pythonProcess = spawn('python', ['./scripts/get_file_path.py']);
  let scriptOutput = ''; // Pythonからの標準出力を格納
  let errorData = '';

  pythonProcess.stdout.on('data', (data) => {
    scriptOutput += data.toString(); // データを追記
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
    res.json({ filePath: scriptOutput.trim() }); // 最後にまとめてtrimする
  });

  pythonProcess.on('error', (err) => {
    console.error('Failed to start Python subprocess.', err);
    res.status(500).json({ error: 'ファイルパスの取得に失敗しました (Pythonプロセス起動エラー)。' });
  });
});

app.listen(3000, () => {
  console.log('サーバーがポート3000で起動しました。');
});
