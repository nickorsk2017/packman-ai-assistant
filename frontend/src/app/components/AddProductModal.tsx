"use client";

import { useState, FormEvent } from "react";
import { getDeviceDescription } from "../../api/ai";
import { cx } from '@/app/utils';

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
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);
  const [lastAiName, setLastAiName] = useState<string | null>(null);

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
    setAiLoading(false);
    setAiError(null);
    setLastAiName(null);
    onClose();
  };

  if (!open) return null;

  const containerHeightClass = step === 2 ? "h-[90vh]" : "";

  return (
    <div
      className="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 backdrop-blur-sm px-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="add-product-title"
    >
      <div
        className={`max-h-[700px] flex w-full max-w-[600px] flex-col rounded-3xl bg-white p-6 shadow-2xl sm:p-8 ${containerHeightClass}`}
      >
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

        <form onSubmit={handleSubmit} className="mt-6 flex h-full flex-col">
          <div className="flex-1 space-y-6 overflow-y-auto">
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
              <div className="flex h-full flex-col space-y-4">
                {!aiLoading &&<div className="flex-1 flex flex-col">
                  <label
                    htmlFor="product-description"
                    className="block text-xs font-semibold uppercase tracking-wider text-[var(--muted)]"
                  >
                    Description <span className="font-normal text-[var(--muted)]">(optional)</span>
                  </label>
                  <textarea
                    id="product-description"
                    value={form.description}
                    onChange={(e) => setForm((prev) => ({ ...prev, description: e.target.value }))}
                    placeholder="Brief description or key features"
                    className="mt-1 w-full flex-1 min-h-[260px] resize-none rounded-xl border border-[var(--lilac-200)] bg-white px-3 py-2 text-sm text-[var(--foreground)] shadow-sm outline-none focus:border-[var(--lilac-500)] focus:ring-2 focus:ring-[var(--lilac-300)]"
                  />
                </div>}
                {aiLoading && (
                  <p className="flex-1 flex items-center justify-center gap-2 text-[22px] text-[var(--muted)]">
                    <span className="inline-block h-8 w-8 animate-spin rounded-full border border-[var(--lilac-400)] border-t-transparent" />
                    <span>Generating description with AI…</span>
                  </p>
                )}
                {aiError && (
                  <p className="text-xs text-red-600">
                    Couldn&apos;t fetch AI description: {aiError}
                  </p>
                )}
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
          </div>

          <div className="mt-6 flex justify-between gap-3">
            <button
              type="button"
              onClick={handleClose}
              disabled={step === 2 && aiLoading}
              className={cx(!aiLoading && "cursor-pointer", "rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)] disabled:opacity-60", step === 2 && aiLoading && "opacity-60 cursor-not-allowed")}
            >
              Cancel
            </button>

            <div className="flex gap-3">
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep((prev) => (prev > 1 ? ((prev - 1) as 1 | 2 | 3) : prev))}
                  disabled={step === 2 && aiLoading}
                  className={cx(!aiLoading && "cursor-pointer", "rounded-xl border border-[var(--lilac-200)] bg-white px-4 py-2 text-sm font-medium text-[var(--foreground)] hover:bg-[var(--lilac-50)] disabled:opacity-60", step === 2 && aiLoading && "opacity-60 cursor-not-allowed")}
                >
                  Back
                </button>
              )}

              {step < 3 && (
                <button
                  type="button"
                  disabled={(step === 1 && !form.name.trim()) || (step === 2 && aiLoading)}
                  onClick={async () => {
                    if (step === 1) {
                      const trimmed = form.name.trim();
                      if (!trimmed) return;
                      setStep(2);
                      // Only call AI if we haven't already for this name
                      if (lastAiName === trimmed || form.description.trim()) return;
                      try {
                        setAiLoading(true);
                        setAiError(null);
                        const res = await getDeviceDescription(trimmed);
                        setForm((prev) => ({
                          ...prev,
                          description: prev.description || res.description,
                        }));
                        setLastAiName(trimmed);
                      } catch (e) {
                        setAiError(e instanceof Error ? e.message : "Unknown error");
                      } finally {
                        setAiLoading(false);
                      }
                    } else {
                      setStep((prev) => (prev < 3 ? ((prev + 1) as 1 | 2 | 3) : prev));
                    }
                  }}
                  className={cx(!aiLoading && "cursor-pointer", "rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)] disabled:opacity-60", aiLoading && "opacity-60 cursor-not-allowed")}
                >
                  Next
                </button>
              )}

              {step === 3 && (
                <button
                  type="submit"
                  disabled={aiLoading}
                  className={cx(!aiLoading && "cursor-pointer", "rounded-xl bg-[var(--lilac-500)] px-4 py-2 text-sm font-semibold text-white shadow-md hover:bg-[var(--lilac-600)] disabled:opacity-60",  aiLoading && "opacity-60 cursor-not-allowed")}
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
