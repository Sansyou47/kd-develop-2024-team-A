const express = require('express');
const multer = require('multer');
const { Rembg } = require('rembg-node');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// multer設定（画像アップロード用）
const upload = multer({ dest: 'uploads/' });

// rembgインスタンス
const rembg = new Rembg();

app.post('/upload', upload.single('image'), async (req, res) => {
    try {
        const inputPath = req.file.path;
        const outputPath = [`output-${Date.now()}.webp`](command: _github.copilot.openSymbolFromReferences ?% 5B % 7B % 22 % 24mid % 22 % 3A1 % 2C % 22fsPath % 22 % 3A % 22 % 2FUsers % 2Fyomesaka % 2FDocuments % 2Fsrc % 2Fkd - develop - 2024 - team - A % 2Fpython % 2Fapp % 2Ftemplates % 2Ftest.js % 22 % 2C % 22external % 22 % 3A % 22file % 3A % 2F % 2F % 2FUsers % 2Fyomesaka % 2FDocuments % 2Fsrc % 2Fkd - develop - 2024 - team - A % 2Fpython % 2Fapp % 2Ftemplates % 2Ftest.js % 22 % 2C % 22path % 22 % 3A % 22 % 2FUsers % 2Fyomesaka % 2FDocuments % 2Fsrc % 2Fkd - develop - 2024 - team - A % 2Fpython % 2Fapp % 2Ftemplates % 2Ftest.js % 22 % 2C % 22scheme % 22 % 3A % 22file % 22 % 7D % 2C % 7B % 22line % 22 % 3A14 % 2C % 22character % 22 % 3A4 % 7D % 5D "python/app/templates/test.js");

        // sharpで画像を読み込み
        const inputBuffer = await sharp(inputPath).toBuffer();

        // rembgで背景を削除
        const outputBuffer = await rembg.remove(inputBuffer);

        // 結果をファイルに保存
        await sharp(outputBuffer).toFile(outputPath);

        // 結果の画像をクライアントに返す
        res.sendFile(path.join(__dirname, outputPath), () => {
            // 使用後のファイルを削除
            fs.unlinkSync(inputPath);
            fs.unlinkSync(outputPath);
        });
    } catch (error) {
        console.error(error);
        res.status(500).send('エラーが発生しました');
    }
});

app.listen(port, () => {
    console.log(`サーバーがポート${port}で起動しました。`);
});