import React from 'react';
import { useEffect, useState } from 'react';

import ProductHeader from './product_header';
import ProductRow from './product_row';


interface ProductListJSON {
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

export enum Discount {
    None = 'NONE',
    Normal = 'NORMAL',
    Member = 'MEMBER'
}

export const ProductList = () => {
    const list_offset = 100;
    const list_length = 100;
    const reverse_order = true;

    const stores = ['Coop', 'Maxima', 'Prisma', 'Rimi', 'Selver'];
    const status_style = 'py-5 text-center tracking-wider text-base';
    const item_layout = 'inline-block min-w-[3.5em] sm:min-w-[5em] sm:w-[5em] mt-1 ml-1 md:mt-0 text-center';

    const [error, setError] = useState<{message: string} | null>(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [items, setItems] = useState<ProductListJSON | []>([]);

    useEffect(() => {
        const base_url = `${location.protocol}//${location.hostname}:8001/api/v1/products/?`;
        const query = `limit=${list_length}&offset=${list_offset}&reverse=${reverse_order}`;
        fetch(base_url + query, {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(
                (result) => { setItems(result); setIsLoaded(true); },
                (error) => { setError(error); setIsLoaded(true); }
            )
    }, []);

    return (
        <div className="row-start-3 xl:row-start-auto xl:row-span-3 col-span-10 xl:col-span-7 bg-transparent text-stone-800">
            <div className="shadow-sm cursor-default pb-2 bg-stone-50 text-sm lg:text-base">
                <ProductHeader stores={stores} item_layout={item_layout} />
                {isLoaded ? (items as ProductListJSON).results?.map(p => {
                    let product = new Product(p)
                    return <ProductRow key={product.id} stores={stores} product={product} item_layout={item_layout} />;
                }) : <div className={`${status_style}`}>Laeme...</div>}
                {error ? <div className={`${status_style}`}>Error! {error.message}</div> : <></>}
            </div>
        </div>
    );
}

export default ProductList;
