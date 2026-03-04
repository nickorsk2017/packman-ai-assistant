const getAiBaseUrl = () => "http://localhost:8001/api/v1";

export type DeviceDescription = {
  name: string;
  description: string;
};

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    let message = text;
    try {
      const json = JSON.parse(text) as { detail?: string };
      if (typeof json.detail === "string") message = json.detail;
    } catch {
      // fall back to raw text
    }
    throw new Error(message || `HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function getDeviceDescription(name: string): Promise<DeviceDescription> {
  const url = new URL(`${getAiBaseUrl()}/device/description`);
  url.searchParams.set("name", name);
  const res = await fetch(url.toString());
  return handleResponse<DeviceDescription>(res);
}

