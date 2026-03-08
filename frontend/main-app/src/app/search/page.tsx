"use client";

import { useState } from "react";
import { 
  SearchPageHeader, 
  SearchFiltersSidebar, 
  SearchPromptSection, 
  AddDeviceModal, 
  type AddDeviceFormData 
} from "@/features/search";
import { createDevice } from "@/services/devices";
import { indexDevice, searchDevices, type DeviceSearchResult } from "@/services/ai";

const CATEGORIES = [{ id: "phones", label: "Phones" as const }];
const ITEM_COUNT = 100;

export default function SearchPage() {
  const [prompt, setPrompt] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [selectedCategory] = useState(CATEGORIES[0]);
  const [addDeviceOpen, setAddDeviceOpen] = useState(false);
  const [addDeviceError, setAddDeviceError] = useState<string | null>(null);
  const [askLoading, setAskLoading] = useState(false);
  const [askError, setAskError] = useState<string | null>(null);
  const [bestMatch, setBestMatch] = useState<DeviceSearchResult | null>(null);
  const [noMatchFound, setNoMatchFound] = useState(false);

  const handleAskPackMan = async () => {
    const q = prompt.trim();
    if (!q) return;
    setAskError(null);
    setBestMatch(null);
    setNoMatchFound(false);
    setAskLoading(true);
    try {
      const res = await searchDevices(q, 1);
      const top = res.devices[0] ?? null;
      setBestMatch(top);
      setNoMatchFound(!top);
    } catch (err) {
      setAskError(err instanceof Error ? err.message : "Search failed");
    } finally {
      setAskLoading(false);
    }
  };

  const handleAddDevice = async (data: AddDeviceFormData) => {
    setAddDeviceError(null);
    try {
      const device = await createDevice({
        name: data.name,
        category: data.category,
        price: data.price ? parseFloat(data.price) : 0,
        description: data.description || null,
      });
      await indexDevice({
        name: device.name,
        description: device.description ?? undefined,
        price: device.price,
        category: device.category,
      });
      setAddDeviceOpen(false);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to add device";
      setAddDeviceError(message);
      throw err;
    }
  };

  return (
    <>
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        <SearchPageHeader />

        <div className="mt-10 grid gap-8 md:grid-cols-[220px,minmax(0,1fr)]">
          <SearchFiltersSidebar
            selectedCategory={selectedCategory}
            maxPrice={maxPrice}
            onMaxPriceChange={setMaxPrice}
          />
          <SearchPromptSection
            selectedCategory={selectedCategory}
            itemCount={ITEM_COUNT}
            prompt={prompt}
            onPromptChange={setPrompt}
            onAddDeviceClick={() => setAddDeviceOpen(true)}
            onAskClick={handleAskPackMan}
            askLoading={askLoading}
            bestMatch={bestMatch}
            askError={askError}
            noMatchFound={noMatchFound}
          />
        </div>
      </div>

      <AddDeviceModal
        open={addDeviceOpen}
        onClose={() => {
          setAddDeviceOpen(false);
          setAddDeviceError(null);
        }}
        onSubmit={handleAddDevice}
        error={addDeviceError}
      />
    </>
  );
}
