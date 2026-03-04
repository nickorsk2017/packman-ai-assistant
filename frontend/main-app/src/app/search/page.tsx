"use client";

import { useState } from "react";
import { 
  SearchPageHeader, 
  SearchFiltersSidebar, 
  SearchPromptSection, 
  AddProductModal, 
  type AddProductFormData 
} from "@/features/search";
import { createProduct } from "@/services/products";
import { Header, Footer } from "@/shared/ui/layout";

const CATEGORIES = [{ id: "phones", label: "Phones" as const }];
const ITEM_COUNT = 100;

export default function SearchPage() {
  const [prompt, setPrompt] = useState("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  const [selectedCategory] = useState(CATEGORIES[0]);
  const [addProductOpen, setAddProductOpen] = useState(false);
  const [addProductError, setAddProductError] = useState<string | null>(null);

  const handleAddProduct = async (data: AddProductFormData) => {
    setAddProductError(null);
    try {
      await createProduct({
        name: data.name,
        category: data.category,
        price: data.price ? parseFloat(data.price) : 0,
        description: data.description || null,
      });
      setAddProductOpen(false);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to add product";
      setAddProductError(message);
      throw err;
    }
  };

  return (
    <div className="min-h-screen gradient-mesh bg-[var(--background)] text-[var(--foreground)]">
      <Header />

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

      <Footer />

      <AddProductModal
        open={addProductOpen}
        onClose={() => {
          setAddProductOpen(false);
          setAddProductError(null);
        }}
        onSubmit={handleAddProduct}
        error={addProductError}
      />
    </div>
  );
}
