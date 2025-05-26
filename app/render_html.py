import os
import json
from pathlib import Path

def render_life_html(life_data: dict, output_path: str, file_prefix: str):
    def escape(text):
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    html = [
        "<html><head><meta charset='UTF-8'><title>Life Overview</title><style>",
        "body { font-family: Arial, sans-serif; margin: 2rem; }",
        "summary { font-weight: bold; font-size: 1.1rem; cursor: pointer; }",
        "details { margin-bottom: 1em; }",
        "ul { margin: 0.5rem 0 0.5rem 1.5rem; }",
        ".crm { border-top: 2px solid #ccc; padding-top: 1rem; margin-top: 2rem; }",
        "</style></head><body><h1>📂 Life Overview</h1>"
    ]

    html.append(f"<a href={file_prefix}.json>JSON File</a><br>")
    html.append(f"<a href={file_prefix}.yaml>YAML File</a><br>")
    # Areas of Responsibility
    for aor in life_data.get("areas_of_responsibility", []):
        html.append(f"<details><summary>🗂 {escape(aor['name'])}</summary>")
        for project in aor.get("projects", []):
            html.append(f"<details class='project'><summary>{escape(project['title'])}</summary>")
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

    # CRM
    crm = life_data.get("crm", {})
    customers = crm.get("customers", [])
    if customers:
        html.append("<div class='crm'><h2>🧑‍💼 CRM</h2>")
        for customer in customers:
            html.append(f"<details><summary>{escape(customer['name'])}</summary>")
            html.append("<ul>")
            html.append(f"<li><strong>Website:</strong> <a href='{escape(customer['website'])}'>{escape(customer['website'])}</a></li>")
            for contact in customer.get("contacts", []):
                html.append(f"<li><strong>Contact:</strong> {escape(contact['name'])} – {escape(contact['title'])} ({escape(contact['email'])}, {escape(contact.get('phone', ''))})</li>")
            for note in customer.get("notes", []):
                if isinstance(note, dict):
                    html.append(f"<li><strong>Note ({escape(note['date'])}):</strong> {escape(note['content'])}</li>")
                else:
                    html.append(f"<li><strong>Note:</strong> {escape(note)}</li>")
            for step in customer.get("next_steps", []):
                if "due" in step:
                    html.append(f"<li><strong>Next Step:</strong> {escape(step['description'])} (due: {escape(step['due'])})</li>")
                else:
                    html.append(f"<li><strong>Next Step:</strong> {escape(step['description'])}</li>")
            html.append("</ul></details>")
        html.append("</div>")

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
</script>
</body></html>
""")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
