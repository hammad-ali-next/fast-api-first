/*
  Warnings:

  - You are about to drop the column `image_base64` on the `Blogs` table. All the data in the column will be lost.
  - Added the required column `image_url` to the `Blogs` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Blogs" DROP COLUMN "image_base64",
ADD COLUMN     "image_url" TEXT NOT NULL;
