import os
import json
from typing import List
from config import ROOT_DIR


def get_cache_path() -> str:
    """
    Gets the path to the cache directory.

    Returns:
        str: Path to the cache directory.
    """
    return os.path.join(ROOT_DIR, ".mp")


def get_cache_file_path(file_name: str) -> str:
    """
    Constructs the full path for a cache file.

    Args:
        file_name (str): Name of the cache file.

    Returns:
        str: Full path to the cache file.
    """
    return os.path.join(get_cache_path(), file_name)


# Specific cache paths
def get_afm_cache_path() -> str:
    return get_cache_file_path("afm.json")


def get_twitter_cache_path() -> str:
    return get_cache_file_path("twitter.json")


def get_youtube_cache_path() -> str:
    return get_cache_file_path("youtube.json")


# Account management
def get_accounts(provider: str) -> List[dict]:
    """
    Retrieves accounts from the specified cache file.

    Args:
        provider (str): The provider ("twitter" or "youtube").

    Returns:
        List[dict]: List of accounts.
    """
    cache_path = (
        get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()
    )

    if not os.path.exists(cache_path):
        # Initialize cache file if it doesn't exist
        with open(cache_path, "w") as file:
            json.dump({"accounts": []}, file, indent=4)

    with open(cache_path, "r") as file:
        data = json.load(file)
        return data.get("accounts", [])


def add_account(provider: str, account: dict) -> None:
    """
    Adds a new account to the specified provider cache.

    Args:
        provider (str): The provider ("twitter" or "youtube").
        account (dict): The account details to add.

    Returns:
        None
    """
    accounts = get_accounts(provider)
    accounts.append(account)

    cache_path = (
        get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()
    )
    with open(cache_path, "w") as file:
        json.dump({"accounts": accounts}, file, indent=4)


def remove_account(provider: str, account_id: str) -> None:
    """
    Removes an account from the specified provider cache.

    Args:
        provider (str): The provider ("twitter" or "youtube").
        account_id (str): The ID of the account to remove.

    Returns:
        None
    """
    accounts = get_accounts(provider)
    accounts = [account for account in accounts if account["id"] != account_id]

    cache_path = (
        get_twitter_cache_path() if provider == "twitter" else get_youtube_cache_path()
    )
    with open(cache_path, "w") as file:
        json.dump({"accounts": accounts}, file, indent=4)


# Product management
def get_products() -> List[dict]:
    """
    Retrieves the list of products from the cache.

    Returns:
        List[dict]: List of products.
    """
    if not os.path.exists(get_afm_cache_path()):
        # Initialize product cache if it doesn't exist
        with open(get_afm_cache_path(), "w") as file:
            json.dump({"products": []}, file, indent=4)

    with open(get_afm_cache_path(), "r") as file:
        data = json.load(file)
        return data.get("products", [])


def add_product(product: dict) -> None:
    """
    Adds a product to the cache.

    Args:
        product (dict): Product details to add.

    Returns:
        None
    """
    products = get_products()
    products.append(product)

    with open(get_afm_cache_path(), "w") as file:
        json.dump({"products": products}, file, indent=4)


# General cache paths
def get_results_cache_path() -> str:
    """
    Gets the path to the results cache file.

    Returns:
        str: Path to the results cache file.
    """
    return get_cache_file_path("scraper_results.csv")
