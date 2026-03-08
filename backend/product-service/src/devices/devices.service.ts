import { Injectable, NotFoundException } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { Device } from "./device.entity";
import { CreateDeviceDto } from "./dto/create-device.dto";
import { UpdateDeviceDto } from "./dto/update-device.dto";

@Injectable()
export class DevicesService {
  constructor(
    @InjectRepository(Device)
    private readonly repo: Repository<Device>
  ) {}

  async findAll(category?: string): Promise<Device[]> {
    const qb = this.repo.createQueryBuilder("device");
    if (category) {
      qb.where("device.category = :category", { category });
    }

    return qb.orderBy("device.createdAt", "DESC").getMany();
  }

  async findOne(id: number): Promise<Device> {
    const device = await this.repo.findOne({ where: { id } });
    if (!device) {
      throw new NotFoundException("Device not found");
    }
    return device;
  }

  async create(dto: CreateDeviceDto): Promise<Device> {
    const entity = this.repo.create({
      name: dto.name,
      category: dto.category,
      price: dto.price,
      description: dto.description ?? null,
    });
    return this.repo.save(entity);
  }

  async update(id: number, dto: UpdateDeviceDto): Promise<Device> {
    const device = await this.findOne(id);
    Object.assign(device, dto);
    return this.repo.save(device);
  }

  async remove(id: number): Promise<void> {
    const device = await this.findOne(id);
    await this.repo.remove(device);
  }
}
