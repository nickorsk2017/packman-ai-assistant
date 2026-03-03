"use client";

import { useState, FormEvent } from "react";

const CATEGORIES = [{ id: "phones", label: "Phones" }];

export type AddProductFormData = {
  name: string;
  category: string;
  price: string;
  description: string;
};

type AddProductModalProps = {
  open: boolean;
  onClose: () => void;
  onSubmit?: (data: AddProductFormData) => Promise<void> | void;
  error?: string | null;
};

const initialForm: AddProductFormData = {
  name: "",
  category: CATEGORIES[0].id,
  price: "",
  description: "",
};

export function AddProductModal({ open, onClose, onSubmit, error }: AddProductModalProps) {
  const [form, setForm] = useState<AddProductFormData>(initialForm);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      await onSubmit?.(form);
      setForm(initialForm);
      onClose();
    } catch {
      // Error is handled and displayed by the parent via the error prop; keep modal open
    }
  };

  const handleClose = () => {
    setForm(initialForm);
    onClose();
  };

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 backdrop-blur-sm px-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="add-product-title"
    >
      <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl sm:p-8">
        <h2 id="add-product-title" className="text-xl font-semibold text-[var(--foreground)] sm:text-2xl">
          Add Product
        </h2>
        <p className="mt-1 text-sm text-[var(--muted)]">
          Add a product to the catalog for AI search.
        </p>

        {error && (
          <p className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="product-name" className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
              Product name
            </label>
            <input
              id="product-name"
              type="text"
              required
              value={form.name}
              onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
              placeholder="e.g. iPhone 15 Pro"
              className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
            />
          </div>

          <div>
            <label htmlFor="product-category" className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
              Category
            </label>
            <select
              id="product-category"
              value={form.category}
              onChange={(e) => setForm((prev) => ({ ...prev, category: e.target.value }))}
              className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat.id} value={cat.id}>
                  {cat.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="product-price" className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
              Price (USD)
            </label>
            <input
              id="product-price"
              type="number"
              min={0}
              step={0.01}
              value={form.price}
              onChange={(e) => setForm((prev) => ({ ...prev, price: e.target.value }))}
              placeholder="e.g. 999"
              className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
            />
          </div>

          <div>
            <label htmlFor="product-description" className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]">
              Description <span className="font-normal text-[var(--muted)]">(optional)</span>
            </label>
            <textarea
              id="product-description"
              rows={3}
              value={form.description}
              onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
              placeholder="Brief description or specs"
              className="mt-1 w-full resize-y rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
            />
          </div>

          <div className="mt-6 flex justify-end gap-3">
            <button
              type="button"
              onClick={handleClose}
              className="rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)]"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)]"
            >
              Add Product
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
