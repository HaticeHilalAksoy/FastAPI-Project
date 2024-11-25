const apiUrl = "http://127.0.0.1:8015";

async function fetchTasks() {
  const response = await fetch(`${apiUrl}/tasks`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json"
    }
  });

  if (response.ok) {
    const tasks = await response.json();
    const taskTableBody = document.getElementById("task-table-body");
    taskTableBody.innerHTML = "";

    tasks.forEach((task) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${task.title}</td>
        <td>${task.description || "-"}</td>
        <td>${task.date}</td>
        <td>${task.duration} saat</td>
        <td>${task.is_completed ? "Evet" : "Hayır"}</td>
        <td>
          <button onclick="deleteTask(${task.id})">Sil</button>
          <button onclick="completeTask(${task.id})">Tamamla</button>
        </td>
      `;
      taskTableBody.appendChild(row);
    });
  } else {
    alert("Görevler alınırken bir hata oluştu: " + response.statusText);
  }
}

async function createTask() {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;
  const date = document.getElementById("date").value;
  const duration = document.getElementById("duration").value;
  const reminderTime = document.getElementById("reminder_time").value || null;

  const newTask = {
    title,
    description,
    date,
    duration: parseInt(duration),
    is_completed: false,
    reminder_time: reminderTime,
  };

  try {
    const response = await fetch(`${apiUrl}/tasks`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(newTask),
    });

    if (response.ok) {
      alert("Görev başarıyla eklendi!");
      fetchTasks(); // Görevleri yeniden yükle
    } else {
      const errorData = await response.json();
      alert(`Hata: ${errorData.detail}`);
    }
  } catch (error) {
    console.error("Görev eklenirken hata oluştu:", error);
  }
}

async function deleteTask(taskId) {
  try {
    const response = await fetch(`${apiUrl}/tasks/${taskId}`, {
      method: "DELETE"
    });

    if (response.ok) {
      alert("Görev başarıyla silindi!");
      fetchTasks(); // Görevleri yeniden yükle
    } else {
      alert("Görev silinirken bir hata oluştu.");
    }
  } catch (error) {
    console.error("Görev silinirken hata oluştu:", error);
  }
}

async function completeTask(taskId) {
  try {
    const response = await fetch(`${apiUrl}/tasks/${taskId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ is_completed: true })
    });

    if (response.ok) {
      alert("Görev tamamlandı!");
      fetchTasks(); // Görevleri yeniden yükle
    } else {
      alert("Görev güncellenirken bir hata oluştu.");
    }
  } catch (error) {
    console.error("Görev güncellenirken hata oluştu:", error);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();

  document.getElementById("add-task-btn").addEventListener("click", async () => {
    await createTask();
  });

  document.getElementById("download-report-btn").addEventListener("click", async () => {
    // Haftalık raporu al
    const response = await fetch(`${apiUrl}/report`);
    if (response.ok) {
      const report = await response.json();
      // JSON dosyasını indir
      const blob = new Blob([JSON.stringify(report, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "weekly_report.json";
      a.click();
      URL.revokeObjectURL(url);
    } else {
      alert("Rapor alınırken bir hata oluştu.");
    }
  });
});
