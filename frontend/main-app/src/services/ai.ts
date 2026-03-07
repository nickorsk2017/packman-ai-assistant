const getAiBaseUrl = () => "http://localhost:8001/api/v1";

export type DeviceDescription = {
  name: string;
  description: string;
};

export type DeviceIndexPayload = {
  name: string;
  description?: string | null;
  price?: number | null;
  category?: string | null;
};

export type DeviceIndexResponse = {
  name: string;
  tags: string[];
  indexed: boolean;
};

export type DeviceSearchResult = {
  name: string;
  tags: string[];
  price?: number | null;
  category: string;
};

export type DeviceSearchResponse = {
  prompt: string;
  devices: DeviceSearchResult[];
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

/** Add device to FAISS vector DB; OpenAI generates tags from name/description. */
export async function indexDevice(payload: DeviceIndexPayload): Promise<DeviceIndexResponse> {
  const res = await fetch(`${getAiBaseUrl()}/device/index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<DeviceIndexResponse>(res);
}

/** Find devices by prompt/tags using FAISS similarity search. */
export async function searchDevices(
  prompt: string,
  k: number = 5
): Promise<DeviceSearchResponse> {
  const url = new URL(`${getAiBaseUrl()}/device/search`);
  url.searchParams.set("prompt", prompt);
  url.searchParams.set("k", String(k));
  const res = await fetch(url.toString());
  return handleResponse<DeviceSearchResponse>(res);
}

