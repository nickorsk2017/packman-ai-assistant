const getBaseUrl = () => "http://localhost:3001/api/v1"

export type Device = {
  id: number;
  name: string;
  category: string;
  price: number;
  description: string | null;
  /** API may return created_at (snake) or createdAt (camel) */
  created_at?: string;
  createdAt?: string;
};

export type DeviceCreate = {
  name: string;
  category: string;
  price: number;
  description?: string | null;
};

export type DeviceUpdate = {
  name?: string;
  category?: string;
  price?: number;
  description?: string | null;
};

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    let message = text;
    try {
      const json = JSON.parse(text) as { detail?: string | { msg: string }[] };
      if (typeof json.detail === "string") message = json.detail;
      else if (Array.isArray(json.detail)) message = json.detail.map((d) => d.msg).join(", ");
    } catch {
      // fall back to raw text
    }
    throw new Error(message || `HTTP ${res.status}`);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

export async function listDevices(category?: string): Promise<Device[]> {
  const url = category
    ? `${getBaseUrl()}/devices?category=${encodeURIComponent(category)}`
    : `${getBaseUrl()}/devices`;
  const res = await fetch(url);
  return handleResponse<Device[]>(res);
}

export async function getDevice(id: number): Promise<Device> {
  const res = await fetch(`${getBaseUrl()}/devices/${id}`);
  return handleResponse<Device>(res);
}

export async function createDevice(data: DeviceCreate): Promise<Device> {
  const res = await fetch(`${getBaseUrl()}/devices`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Device>(res);
}

export async function updateDevice(id: number, data: DeviceUpdate): Promise<Device> {
  const res = await fetch(`${getBaseUrl()}/devices/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Device>(res);
}

export async function deleteDevice(id: number): Promise<void> {
  const res = await fetch(`${getBaseUrl()}/devices/${id}`, { method: "DELETE" });
  return handleResponse<void>(res);
}
