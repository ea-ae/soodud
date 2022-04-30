// Product list API

export interface QueryEvents {
    onSuccess: (result: any) => void;
    onError: (error: any) => void;
}

export interface ProductListAPIQuery {
    offset: number;
    length: number;
    reverse: boolean;
    search?: string;
}

export interface ProductListJSON {
    results: ProductJSON[];
}

interface ProductJSON {
    id: number;
    name: string;
    store_products: StoreProduct[];
}

interface StoreProduct {
    store_name: string;
    last_checked: string;
    price: {
        start: string;
        base_price: number;
        price: number;
        type: string;
    }
}

export class Product {
    id: number;
    name: string;
    prices: Prices;

    constructor(json: ProductJSON) {
        this.id = json.id;
        this.name = json.name;
        this.prices = {};
        json.store_products.forEach(sp => {
            this.prices[sp.store_name.toLowerCase()] = {
                basePrice: sp.price.base_price,
                actualPrice: sp.price.price,
                discount: sp.price.type as Discount
            };
        });
    }
}

interface Prices {
    [key: string]: Price;
}

export interface Price {
    basePrice?: number;
    actualPrice: number;
    discount: Discount;
}

// Product detail API

export interface DetailedProduct {
    name: string;
    quantity: {
        amount: number;
        unit: string;
    }[];
    tags: string[];
    store_products: DetailedStoreProduct[];
}

interface DetailedStoreProduct {
    store_name: string;
    name: string;
    last_checked: string;
    prices: DetailedPrice[];
}

interface DetailedPrice {
    start: string;
    base_price: number;
    price: number;
    type: Discount;
}

// Miscellaneous API

export enum Discount {
    None = 'NONE',
    Normal = 'NORMAL',
    Member = 'MEMBER'
}
