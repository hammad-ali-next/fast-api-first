/*
  Warnings:

  - Made the column `user_id` on table `Blogs` required. This step will fail if there are existing NULL values in that column.

*/
-- DropForeignKey
ALTER TABLE "Blogs" DROP CONSTRAINT "Blogs_user_id_fkey";

-- AlterTable
ALTER TABLE "Blogs" ALTER COLUMN "created_date" SET DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN "user_id" SET NOT NULL;

-- AddForeignKey
ALTER TABLE "Blogs" ADD CONSTRAINT "Blogs_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "Users"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
