import os
from werkzeug.utils import secure_filename
from models.models import db, Shelter, Animal, Pet

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    """Check if the uploaded file has an allowed image extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def save_image(file, upload_folder, old_image_path=None):
    """
    Save an uploaded image to the upload folder.
    Optionally delete the old image if provided.
    Returns the saved filename or None if the file is invalid.
    """
    if not file or file.filename == "":
        return None

    if not allowed_file(file.filename):
        return None

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)

    # Remove old image from disk if it exists
    if old_image_path and os.path.exists(old_image_path):
        os.remove(old_image_path)

    file.save(filepath)
    return filename


def save_or_update_shelter(form_data, file, upload_folder, shelter=None):
    """
    Create a new shelter or update an existing one.
    Returns the shelter instance.
    """
    name = form_data["name"]
    address = form_data["address"]
    phone = form_data["phone"]
    email = form_data["email"]
    description = form_data.get("description", "")

    # Handle image upload
    old_image_path = (
        os.path.join(upload_folder, shelter.image)
        if shelter and shelter.image
        else None
    )
    image_filename = save_image(file, upload_folder, old_image_path)

    # Keep existing image if no new one was uploaded
    if not image_filename and shelter:
        image_filename = shelter.image

    if shelter:
        shelter.name = name
        shelter.address = address
        shelter.phone = phone
        shelter.email = email
        shelter.description = description
        shelter.image = image_filename
    else:
        shelter = Shelter(
            name=name,
            address=address,
            phone=phone,
            email=email,
            description=description,
            image=image_filename,
        )
        db.session.add(shelter)

    db.session.commit()
    return shelter


def delete_shelter(shelter_id):
    """Delete a shelter by ID."""
    shelter = Shelter.query.get_or_404(shelter_id)
    db.session.delete(shelter)
    db.session.commit()


def save_or_update_animal(form_data, animal=None):
    """Create a new animal entry or update an existing one."""
    species = form_data["species"]
    breed = form_data["breed"]
    lifespan = form_data.get("lifespan", "")
    diet = form_data.get("diet", "")
    specifics = form_data.get("specifics", "")
    image = form_data.get("image", "")

    if animal:
        animal.species = species
        animal.breed = breed
        animal.lifespan = lifespan
        animal.diet = diet
        animal.specifics = specifics
        animal.image = image
    else:
        animal = Animal(
            species=species,
            breed=breed,
            lifespan=lifespan,
            diet=diet,
            specifics=specifics,
            image=image,
        )
        db.session.add(animal)

    db.session.commit()
    return animal


def delete_animal(animal_id):
    """Delete an animal entry by ID."""
    animal = Animal.query.get_or_404(animal_id)
    db.session.delete(animal)
    db.session.commit()


def save_or_update_pet(form_data, pet=None):
    """Create a new pet or update an existing one."""
    if pet:
        pet.name = form_data["name"]
        pet.age = int(form_data["age"])
        pet.gender = form_data["gender"]
        pet.description = form_data.get("description", "")
        pet.adoption_date = form_data.get("adoption_date", None)
        pet.image = form_data.get("image", "")
        pet.shelter_id = int(form_data["shelter_id"])
        pet.animal_id = int(form_data["animal_id"])
    else:
        pet = Pet(
            name=form_data["name"],
            age=int(form_data["age"]),
            gender=form_data["gender"],
            description=form_data.get("description", ""),
            adoption_date=form_data.get("adoption_date", None),
            image=form_data.get("image", ""),
            shelter_id=int(form_data["shelter_id"]),
            animal_id=int(form_data["animal_id"]),
        )
        db.session.add(pet)

    db.session.commit()
    return pet


def delete_pet(pet_id):
    """Delete a pet by ID."""
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()