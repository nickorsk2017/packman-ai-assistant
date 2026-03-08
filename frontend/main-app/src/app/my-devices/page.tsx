"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { listDevices, deleteDevice, type Device } from "@/services/devices";

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  } catch {
    return iso;
  }
}

function getCreatedAt(d: Device): string {
  return d.created_at ?? d.createdAt ?? "";
}

function DeviceCard({
  device,
  onDelete,
}: {
  device: Device;
  onDelete: (id: number) => void;
}) {
  const [deleting, setDeleting] = useState(false);

  const handleDelete = async () => {
    if (!confirm(`Remove "${device.name}" from your devices?`)) return;
    setDeleting(true);
    try {
      await deleteDevice(device.id);
      onDelete(device.id);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <article className="rounded-2xl border border-[var(--lilac-200)]/60 bg-white/80 p-5 shadow-sm backdrop-blur-sm transition-shadow hover:shadow-md">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex-1">
          <h3 className="text-lg font-semibold text-[var(--foreground)] truncate">
            {device.name}
          </h3>
          <p className="mt-0.5 text-sm text-[var(--muted)] capitalize">
            {device.category}
          </p>
          {device.description && (
            <p className="mt-2 text-sm text-[var(--muted)] line-clamp-2">
              {device.description}
            </p>
          )}
          <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
            <span className="font-medium text-[var(--lilac-700)]">
              ${Number(device.price).toFixed(2)}
            </span>
            <span className="text-[var(--muted)]">
              Added {formatDate(getCreatedAt(device) || "—")}
            </span>
          </div>
        </div>
        <button
          type="button"
          onClick={handleDelete}
          disabled={deleting}
          className="shrink-0 rounded-full border border-red-200 bg-red-50 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-100 disabled:opacity-50"
        >
          {deleting ? "Removing…" : "Remove"}
        </button>
      </div>
    </article>
  );
}

export default function MyDevicesPage() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDevices = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listDevices();
      setDevices(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load devices");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDevices();
  }, []);

  const removeFromList = (id: number) => {
    setDevices((prev) => prev.filter((d) => d.id !== id));
  };

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 sm:px-6 lg:px-8">
      <Link
        href="/search"
        className="mb-6 inline-flex items-center gap-2 text-sm font-medium text-[var(--muted)] hover:text-[var(--lilac-600)] transition-colors"
      >
        <span aria-hidden>←</span>
        Back to search
      </Link>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-[var(--foreground)] sm:text-4xl">
          My added devices
        </h1>
        <p className="mt-3 text-[var(--muted)]">
          Devices you&apos;ve added to the catalog. Add more from the search page.
        </p>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-16">
          <span className="text-[var(--muted)]">Loading…</span>
        </div>
      )}

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800">
          {error}
          <button
            type="button"
            onClick={loadDevices}
            className="mt-2 font-medium underline"
          >
            Try again
          </button>
        </div>
      )}

      {!loading && !error && devices.length === 0 && (
        <div className="rounded-2xl border border-[var(--lilac-200)]/60 bg-white/60 p-10 text-center">
          <p className="text-[var(--muted)]">You haven&apos;t added any devices yet.</p>
          <Link
            href="/search"
            className="mt-4 inline-flex rounded-full bg-[var(--lilac-500)] px-5 py-2.5 text-sm font-medium text-white hover:bg-[var(--lilac-600)] transition-colors"
          >
            Go to AI Search to add a device
          </Link>
        </div>
      )}

      {!loading && !error && devices.length > 0 && (
        <ul className="space-y-4">
          {devices.map((device) => (
            <li key={device.id}>
              <DeviceCard device={device} onDelete={removeFromList} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
