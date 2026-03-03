"use client";

import { useState, FormEvent } from "react";

const CATEGORIES = [{ id: "phones", label: "Phones" }];

export type AddProductFormData = {
  name: string;
  category: string;
  price: string;
  description: string;
  condition: string;
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
  condition: "",
};

export function AddProductModal({ open, onClose, onSubmit, error }: AddProductModalProps) {
  const [form, setForm] = useState<AddProductFormData>(initialForm);
  const [step, setStep] = useState<1 | 2 | 3>(1);

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
    setStep(1);
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

        <p className="mt-3 text-xs font-medium uppercase tracking-wide text-[var(--muted)]">
          Step {step} of 3 ·{" "}
          {step === 1 && "Product name"}
          {step === 2 && "Description"}
          {step === 3 && "Price & condition"}
        </p>

        {error && (
          <p className="mt-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
            {error}
          </p>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-6">
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="product-name"
                  className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]"
                >
                  Product name
                </label>
                <input
                  id="product-name"
                  type="text"
                  required
                  value={form.name}
                  onChange={(e) => setForm((prev) => ({ ...prev, name: e.target.value }))}
                  placeholder="e.g. iPhone 16 Pro Max"
                  className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="product-description"
                  className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]"
                >
                  Description <span className="font-normal text-[var(--muted)]">(optional)</span>
                </label>
                <textarea
                  id="product-description"
                  rows={4}
                  value={form.description}
                  onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
                  placeholder="Brief description or key features"
                  className="mt-1 w-full resize-y rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="product-price"
                  className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]"
                >
                  Price (USD)
                </label>
                <input
                  id="product-price"
                  type="number"
                  min={0}
                  step={0.01}
                  value={form.price}
                  onChange={(e) => setForm((prev) => ({ ...prev, price: e.target.value }))}
                  placeholder="e.g. 1299"
                  className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                />
              </div>

              <div>
                <label
                  htmlFor="product-condition"
                  className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]"
                >
                  Condition
                </label>
                <select
                  id="product-condition"
                  value={form.condition}
                  onChange={(e) => setForm((prev) => ({ ...prev, condition: e.target.value }))}
                  className="mt-1 w-full rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                >
                  <option value="">Select condition</option>
                  <option value="new">New</option>
                  <option value="like_new">Like new</option>
                  <option value="used_good">Used — good</option>
                  <option value="used_fair">Used — fair</option>
                </select>
              </div>
            </div>
          )}

          <div className="mt-6 flex justify-between gap-3">
            <button
              type="button"
              onClick={handleClose}
              className="rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)]"
            >
              Cancel
            </button>

            <div className="flex gap-3">
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep((prev) => (prev > 1 ? ((prev - 1) as 1 | 2 | 3) : prev))}
                  className="rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)]"
                >
                  Back
                </button>
              )}

              {step < 3 && (
                <button
                  type="button"
                  disabled={step === 1 && !form.name.trim()}
                  onClick={() => setStep((prev) => (prev < 3 ? ((prev + 1) as 1 | 2 | 3) : prev))}
                  className="rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)] disabled:opacity-60"
                >
                  Next
                </button>
              )}

              {step === 3 && (
                <button
                  type="submit"
                  className="rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)]"
                >
                  Add Product
                </button>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
