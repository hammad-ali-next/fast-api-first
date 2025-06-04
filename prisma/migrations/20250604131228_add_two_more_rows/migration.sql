/*
  Warnings:

  - Added the required column `category` to the `Blogs` table without a default value. This is not possible if the table is not empty.
  - Added the required column `image_base64` to the `Blogs` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Blogs" ADD COLUMN     "category" TEXT NOT NULL,
ADD COLUMN     "image_base64" TEXT NOT NULL;
