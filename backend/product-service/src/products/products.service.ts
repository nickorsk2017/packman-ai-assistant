import { Injectable, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { Product } from "./product.entity";
import { CreateProductDto } from "./dto/create-product.dto";
import { UpdateProductDto } from "./dto/update-product.dto";

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private readonly repo: Repository<Product>
  ) {}

  async findAll(category?: string): Promise<Product[]> {
    const qb = this.repo.createQueryBuilder("product");
    if (category) {
      qb.where("product.category = :category", { category });
    }
    
    return qb.orderBy("product.createdAt", "DESC").getMany();
  }

  async findOne(id: number): Promise<Product> {
    const product = await this.repo.findOne({ where: { id } });
    if (!product) {
      throw new NotFoundException("Product not found");
    }
    return product;
  }

  async create(dto: CreateProductDto): Promise<Product> {
    const entity = this.repo.create({
      name: dto.name,
      category: dto.category,
      price: dto.price,
      description: dto.description ?? null,
    });
    return this.repo.save(entity);
  }

  async update(id: number, dto: UpdateProductDto): Promise<Product> {
    const product = await this.findOne(id);
    Object.assign(product, dto);
    return this.repo.save(product);
  }

  async remove(id: number): Promise<void> {
    const product = await this.findOne(id);
    await this.repo.remove(product);
  }
}

