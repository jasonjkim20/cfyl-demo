import logging
import recipes
import random

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)

RECIPE_IMAGES = {
    'AS': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Applesauce-2-1.jpg",
    'AT': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/avocado-toast.jpg",
    'AVS': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Avocado-Smoothie-1.jpg",
    'MS': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/basic-miso-soup.jpg",
    'SCC': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Southwestern-Chicken-Casserole-CFYL-1200x797.jpg",
    'VFR': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Vegetarian-Fired-Rice-CFYL-1.jpg",
    'WS': "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Wonton-Soup-with-Chicken-Mushroom-Dumplings-CFYL-copy.jpg",
    'SEC': "https://s3.amazonaws.com/ask-samples-resources/images/sauce-boss/secret-sauce-500x500.png"
}

RECIPE_DEFAULT_IMAGE = "https://cfyl-s3-assets-us-west-2.s3-us-west-2.amazonaws.com/images/Southwestern-Chicken-Casserole-CFYL-1200x797.jpg"


def get_recipe_item(request):
    """
    Returns an object containing the recipe ID & spoken value by the User from the JSON request
    Values are computed from slot "Item" or from Alexa.Presentation.APL.UserEvent arguments
    """
    recipe_item = {'id': None, 'spoken': None}
    logger.info("get_recipe_item passed request: {}".format(request))
    if(request.object_type == 'Alexa.Presentation.APL.UserEvent'):
        recipe_item['id'] = request.arguments[1]
    else:
        itemSlot = request.intent.slots["Item"]
        # Capture spoken value by the user
        if(itemSlot and itemSlot.value):
            recipe_item['spoken'] = itemSlot.value

        if(itemSlot and
                itemSlot.resolutions and
                itemSlot.resolutions.resolutions_per_authority[0] and
                itemSlot.resolutions.resolutions_per_authority[0].status and
                str(itemSlot.resolutions.resolutions_per_authority[0].status.code) == 'StatusCode.ER_SUCCESS_MATCH'):
            recipe_item['id'] = itemSlot.resolutions.resolutions_per_authority[0].values[0].value.id

    return recipe_item


def get_recipe_image(id):
    """
    Returns the image url of a specified recipe id
    """
    url = RECIPE_IMAGES[id]
    if(url):
        return url
    else:
        return RECIPE_DEFAULT_IMAGE


def get_locale_specific_recipes(locale):
    """
    Returns the recipe dictionary for a specific locale
    """
    return recipes.translations[locale[:2]]


def get_random_recipe(handler_input):
    """
    Returns a random localized recipe from the list of available recipes
    """
    locale = handler_input.request_envelope.request.locale
    randRecipe = random.choice(
        list(get_locale_specific_recipes(locale).items()))
    return randRecipe[1]