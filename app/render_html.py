import os
import json
from pathlib import Path

def render_life_html(life_data: dict, output_path: str, file_prefix: str):
    #def escape(text):
    #    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    def escape(text):
        return (
            str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br>")
        )

    html = [
        "<html><head><meta charset='UTF-8'><title>Life Overview</title><style>",
        "body { font-family: Arial, sans-serif; margin: 2rem; }",
        "summary { font-weight: bold; font-size: 1.1rem; cursor: pointer; }",
        "details { margin-bottom: 1em; }",
        "ul { margin: 0.5rem 0 0.5rem 1.5rem; }",
        ".crm { border-top: 2px solid #ccc; padding-top: 1rem; margin-top: 2rem; }",
        ".project { margin-left: 2rem; }  /* ← ✅ Indent projects under AoRs */",
        "</style></head><body><h1>📂 Life Overview</h1>"
    ]

    html.append("""
<button onclick="toggleDetails()" style="margin-bottom: 1rem;">Collapse All</button>
<div style="margin-bottom: 1rem;">
  <a href="life.json">JSON File</a><br>
  <a href="life.yaml">YAML File</a><br>
</div>
""")
    # Areas of Responsibility
    for aor in life_data.get("areas_of_responsibility", []):
        html.append(f"<details open><summary>🗂 {escape(aor['name'])}</summary>")
        for project in aor.get("projects", []):
            html.append(f"<details open class='project'><summary>{escape(project['title'])}</summary>")
            if project.get("notes"):
                html.append(f"<p><em>{escape(project['notes'])}</em></p>")
            if project.get("tasks"):
                html.append("<ul>")
                for task in project["tasks"]:
                    line = escape(task["description"])
                    if "due" in task:
                        line += f" (due: {escape(task['due'])})"
                    if "customer_id" in task:
                        line += f" [customer_id: {escape(task['customer_id'])}]"
                    html.append(f"<li>{line}</li>")
                html.append("</ul>")
            html.append("</details>")
        html.append("</details>")

    html.append("""
<script>
(function () {
  const interval = 30000;
  let lastModified = null;

  async function checkUpdate() {
    try {
      const response = await fetch(window.location.href, { method: 'HEAD' });
      const newModified = response.headers.get("Last-Modified");

      if (lastModified && newModified !== lastModified) {
        console.log("🔁 Detected update, reloading...");
        location.reload();
      }

      lastModified = newModified;
    } catch (err) {
      console.warn("Error checking for updates:", err);
    }

    setTimeout(checkUpdate, interval);
  }

  checkUpdate();
})();
let expanded = true;

function toggleDetails() {
  const details = document.querySelectorAll("details");
  details.forEach(d => d.open = !expanded);

  const btn = document.querySelector("button");
  btn.textContent = expanded ? "Expand All" : "Collapse All";
  expanded = !expanded;
}

</script>
</body></html>
""")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
