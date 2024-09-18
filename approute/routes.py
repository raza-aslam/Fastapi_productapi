from typing import List, Optional
from fastapi import APIRouter,File, Form, HTTPException,Depends,UploadFile
from sqlmodel import Session, select
from models.product_model import  Product
from Database.setting import engine 
import cloudinary #type:ignore
import cloudinary.uploader #type:ignore
from Database.setting import DB_SESSION
router = APIRouter()



# Create a product
@router.post("/products/")
async def create_product(
    product_name: str = Form(...),
    product_description: str = Form(...),
    category_names: List[str] = Form(...),
    file: Optional[UploadFile] = None,
):
    try:
        # Prepare the product data
        product_data = Product(
            product_name=product_name,
            product_description=product_description,
            category_names=category_names,
        )

        # If an image file is uploaded, upload it to Cloudinary
        if file:
            file_bytes = await file.read()
            upload_result = cloudinary.uploader.upload(file_bytes)
            product_data.product_image = upload_result.get("url")  # Set product_image to the Cloudinary URL

        # Create a new product in the database
        with Session(engine) as session:
            session.add(product_data)
            session.commit()
            session.refresh(product_data)
            return product_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.get("/limited_product/")
def pagination_product():
    with Session(engine) as session:
        statement = select(Product).limit(9)
        results = session.exec(statement).all()
        return results

# Get all products
@router.get("/products/")
def get_products():
    with Session(engine) as session:
        statement = select(Product)
        results = session.exec(statement).all()
        return results

# Get a product by ID
@router.get("/products/{product_id}")
def get_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

# Update a product by ID
@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_name: str = Form(...),
    product_description: str = Form(...),
    category_names: Optional[List[str]] = Form(...),
    file: Optional[UploadFile] = None,
):
    try:
        with Session(engine) as session:
            # Fetch the existing product
            db_product = session.get(Product, product_id)
            if not db_product:
                raise HTTPException(status_code=404, detail="Product not found")

            # Update product fields
            db_product.product_name = product_name
            db_product.product_description = product_description
            db_product.category_names = category_names or []
            # If a new image file is uploaded, upload it to Cloudinary
            if file:
                file_bytes = await file.read()
                upload_result = cloudinary.uploader.upload(file_bytes)
                db_product.product_image = upload_result.get("url")  # Update product_image with the Cloudinary URL

            # Commit the changes to the database
            session.add(db_product)
            session.commit()
            session.refresh(db_product)
            return db_product

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating product: {str(e)}")

# Delete a product by ID
@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        session.delete(product)
        session.commit()
        return {"message": "Product deleted successfully"}

# @router.post("/product_images")
# async def upload_images(file: UploadFile = File(...)):
#     try:
#         # Read the file content asynchronously
#         file_bytes = await file.read()
#         # Upload the file to Cloudinary
#         result = cloudinary.uploader.upload(file_bytes)
#         # Get the URL of the uploaded image
#         uri = result.get("url")
#         return uri
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
