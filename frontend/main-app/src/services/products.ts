const getBaseUrl = () => "http://localhost:3001/api/v1"

export type Product = {
  id: number;
  name: string;
  category: string;
  price: number;
  description: string | null;
  created_at: string;
};

export type ProductCreate = {
  name: string;
  category: string;
  price: number;
  description?: string | null;
};

export type ProductUpdate = {
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

export async function getProduct(id: number): Promise<Product> {
  const res = await fetch(`${getBaseUrl()}/products/${id}`);
  return handleResponse<Product>(res);
}

export async function createProduct(data: ProductCreate): Promise<Product> {
  const res = await fetch(`${getBaseUrl()}/products`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Product>(res);
}

export async function updateProduct(id: number, data: ProductUpdate): Promise<Product> {
  const res = await fetch(`${getBaseUrl()}/products/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse<Product>(res);
}

export async function deleteProduct(id: number): Promise<void> {
  const res = await fetch(`${getBaseUrl()}/products/${id}`, { method: "DELETE" });
  return handleResponse<void>(res);
}

