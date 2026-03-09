import { MigrationInterface, QueryRunner } from "typeorm";

export class CreateDivicesTable1773022215875 implements MigrationInterface {
    name = 'CreateDivicesTable1773022215875'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "devices" ("id" SERIAL NOT NULL, "name" character varying(255) NOT NULL, "category" character varying(100) NOT NULL, "price" numeric(10,2) NOT NULL, "description" text, "created_at" TIMESTAMP NOT NULL DEFAULT now(), CONSTRAINT "PK_b1514758245c12daf43486dd1f0" PRIMARY KEY ("id"))`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`DROP TABLE "devices"`);
    }

}
