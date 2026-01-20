const BASE_URL = "/api";
const API_TOKEN = "devtoken"; // Replace with your actual API token

const headers = {
  "Content-Type": "application/json",
  "X-API-TOKEN": API_TOKEN,
};

export async function getDevices() {
  const response = await fetch(`${BASE_URL}/devices`, { headers });
  if (!response.ok) {
    throw new Error("Failed to fetch devices");
  }
  return await response.json();
}

export async function runScript(device_id: number, script_name: string) {
  const response = await fetch(`${BASE_URL}/scripts/run`, {
    method: "POST",
    headers,
    body: JSON.stringify({ device_id, script_name }),
  });
  if (!response.ok) {
    throw new Error("Failed to run script");
  }
  return await response.json();
}

export async function getExecution(id: number) {
  const response = await fetch(`${BASE_URL}/executions/${id}`, { headers });
  if (!response.ok) {
    throw new Error("Failed to fetch execution");
  }
  return await response.json();
}
