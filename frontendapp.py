import { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    calorie_min: 2000,
    protein_min: 50,
    fat_max: 70,
    carb_min: 250,
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: Number(e.target.value) });
  };

  const handleSubmit = async () => {
    try {
      const res = await axios.post("http://localhost:5000/optimize-diet", form);
      setResult(res.data);
    } catch (err) {
      alert("Çözüm bulunamadı.");
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Diyet Planlayıcı</h1>
      <div className="space-y-2">
        {["calorie_min", "protein_min", "fat_max", "carb_min"].map((key) => (
          <div key={key}>
            <label className="block">{key.replace("_", " ").toUpperCase()}</label>
            <input
              type="number"
              name={key}
              value={form[key]}
              onChange={handleChange}
              className="border p-2 w-full"
            />
          </div>
        ))}
        <button onClick={handleSubmit} className="bg-blue-500 text-white p-2 mt-2">
          Hesapla
        </button>
      </div>
      {result && (
        <div className="mt-6">
          <h2 className="font-semibold mb-2">Sonuç:</h2>
          <ul>
            {Object.entries(result).map(([k, v]) => (
              <li key={k}>
                <strong>{k}:</strong> {v} {k === "toplam_maliyet" ? "₺" : "g"}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
