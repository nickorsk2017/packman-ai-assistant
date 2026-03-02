"use client";

import { useState } from "react";
import { LandingHeader } from "../components/LandingHeader";
import { LandingFooter } from "../components/LandingFooter";
import { SearchPageHeader } from "../components/SearchPageHeader";
import { SearchFiltersSidebar } from "../components/SearchFiltersSidebar";
import { SearchPromptSection } from "../components/SearchPromptSection";
import { AddProductModal, type AddProductFormData } from "../components/AddProductModal";

const CATEGORIES = [{ id: "phones", label: "Phones" as const }];
const ITEM_COUNT = 100;

export default function SearchPage() {
  const [prompt, setPrompt] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [selectedCategory] = useState(CATEGORIES[0]);
  const [addProductOpen, setAddProductOpen] = useState(false);

  const handleAddProduct = (data: AddProductFormData) => {
    console.log("Add product:", data);
  };

  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <LandingHeader />

      <main className="pt-24 pb-16">
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
              onAddProductClick={() => setAddProductOpen(true)}
            />
          </div>
        </div>
      </main>

      <LandingFooter />

      <AddProductModal
        open={addProductOpen}
        onClose={() => setAddProductOpen(false)}
        onSubmit={handleAddProduct}
      />
    </div>
  );
}
