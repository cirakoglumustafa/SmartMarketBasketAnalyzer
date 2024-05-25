document.querySelector(".form").addEventListener("submit", async (e) => {
  e.preventDefault();
});

document.querySelector("#process").addEventListener("click", async (e) => {
  e.preventDefault();
  const data = document.querySelector("#data").value;
  const response = await fetch("http://localhost:3000/apriori", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data }),
  });
  const result = await response.json();
  console.log(result);
  renderResult(result);
});

document.querySelector("#clear").addEventListener("click", (e) => {
  e.preventDefault();
  document.querySelector("#data").value = "";
  document.querySelector(".result").innerHTML = "";
});

document.querySelector("#ai").addEventListener("click", async (e) => {
  e.preventDefault();
  const data = document.querySelector("#data").value;
  const response = await fetch("http://localhost:3000/apriori-ai", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ data }),
  });
  const result = await response.json();
  console.log(result);
  renderResult(result);
});


function renderResult(result) {
  const resultContainer = document.querySelector('.result');
  resultContainer.innerHTML = ''; // Önceki sonuçları temizleyin

  result.forEach(rule => {
    const lhs = rule.lhs.join(', '); // Sol öncül
    const rhs = rule.rhs.join(', '); // Sağ soncül
    const confidence = (rule.confidence * 100).toFixed(2); // Güven değeri, yüzde formatında

    const ruleElement = document.createElement('div');
    ruleElement.innerHTML = `<strong>Kural:</strong> Eğer <strong>${lhs}</strong> varsa, <strong>${rhs}</strong> olur. <strong>Güven:</strong> %${confidence}`;
    resultContainer.appendChild(ruleElement);
  });
}

