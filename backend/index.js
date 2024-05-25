const express = require('express');
const apriori = require('apriori');
const cors = require('cors');
const { GoogleGenerativeAI } = require("@google/generative-ai");

const app = express();
const port = 3000;

const genAI = new GoogleGenerativeAI("AIzaSyAS3HHFdtqVficlmJ9r7hmjzGEgoS9LXOY");

app.use(express.json());
app.use(cors());

const categories = "Et ve Balık, Süt ve Süt Ürünleri, Tahıl ve Fırın Ürünleri, Dondurulmuş Ürünler, Atıştırmalıklar ve Tatlılar, Konserve ve İşlenmiş Gıdalar, Bakliyat ve Tahıllar, Baharat ve Soslar, Sebze ve Meyveler, Hazır Gıdalar, Alkollü İçecekler, Alkolsüz İçecekler, Temizlik ve Bakım Ürünleri, Mutfak Ürünleri, Bahçe Ürünleri, Diğer Ev Ürünleri";

async function predictCategory(product) {
  const model = genAI.getGenerativeModel({ model: "gemini-pro" });

  const prompt = `Ürün "${product}" aşağıdaki kategorilerden hangisine ait olabilir: ${categories}`;

  const result = await model.generateContent(prompt);
  const response = await result.response;
  const text = await response.text();
  return text.trim();
}

function calculateApriori(data) {
  const Apriori = new apriori.Algorithm(0.05, 0.05, null);
  const results = Apriori.analyze(data);
  return results.associationRules;
}

async function processApriori(data) {
  const categorizedData = [];

  for (const transaction of data) {
    const categorizedTransaction = [];

    for (const product of transaction) {
      const category = await predictCategory(product);
      console.log(`${product} -> ${category}`);
      categorizedTransaction.push(category);
    }

    categorizedData.push(categorizedTransaction);
  }

  return calculateApriori(categorizedData);
}

app.post('/apriori', async (req, res) => {
  let data = req.body.data;
  data = data.split('\n').map((line) => line.split(',').map((item) => item.trim()).filter((item) => item !== ''));

  const associationRules = calculateApriori(data);
  res.json(associationRules);
});

app.post('/apriori-ai', async (req, res) => {
  let data = req.body.data;
  data = data.split('\n').map((line) => line.split(',').map((item) => item.trim()).filter((item) => item !== ''));

  const associationRules = await processApriori(data);
  res.json(associationRules);
});

app.listen(port, () => {
  console.log(`Sunucu http://localhost:${port} üzerinde çalışıyor.`);
});
