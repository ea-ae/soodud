import React from 'react';
import { useEffect, useState } from 'react';


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

class Product {
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

interface Price {
    basePrice?: number;
    actualPrice: number;
    discount: Discount;
}

enum Discount {
    None = 'NONE',
    Normal = 'NORMAL',
    Member = 'MEMBER'
}

const ProductList = () => {
    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);
    const [items, setItems] = useState<ProductListJSON | []>([]);

    useEffect(() => {
        fetch(`${location.protocol}//${location.hostname}:8001/api/v1/products/?limit=100&offset=27580`,
              {method: 'GET', headers: {'Content-Type': 'text/plain'}})
            .then(res => res.json())
            .then(
                (result) => { setIsLoaded(true); setItems(result); },
                (error) => { setIsLoaded(true); setError(error); }
            )
    }, []);

    const stores = ['Coop', 'Maxima', 'Prisma', 'Rimi', 'Selver'];
    const status_style = 'mt-10 mb-5 text-center tracking-wider text-lg'
    return (
        <div className="row-start-3 xl:row-start-auto xl:row-span-3 col-span-10 xl:col-span-7 bg-transparent text-stone-800">
        <div className="shadow-sm cursor-default lg:px-5 bg-stone-50 text-sm lg:text-base">
            <ProductListHeader stores={stores} />
            {isLoaded ? (items as ProductListJSON).results?.map(p => {
                let product = new Product(p)
                return <ProductRow key={product.id} stores={stores} product={product} />;
            }) : <div className={`${status_style}`}>Loading...</div>}
            {error ? <div className={`${status_style}`}>Error! {(error as {message: string}).message}</div> : <></>}
        </div>
    </div>
    );
}

const ProductListHeader = (props: {stores: string[]}) => {
    return (
        <>
        <div className="group flex justify-center md:justify-end items-center justify-items-center
                        sticky top-0 flex-wrap md:flex-nowrap px-3 py-2 bg-stone-50 text-stone-600">
            <div className="inline-block min-w-[5em] mt-1 md:mt-0 ml-1">
                <span className="mr-3 text-stone-900 text-xs">Tavahind</span>
                <span className="mr-3 text-yellow-400 text-xs">Soodustus</span>
                <span className="mr-6 text-amber-500 text-xs">Kliendikaardiga</span>
            </div>
            <div className="basis-full md:basis-0 md:hidden"></div>
            {props.stores.sort().map(store => <ProductListHeaderStore key={store} storeName={store} />)}
        </div>
        </>
    );
}

const ProductListHeaderStore = (props: {storeName: string}) => {
    return (
        <div className="inline-block min-w-[3.4em] sm:min-w-[5em] sm:w-[5em] mt-1 ml-1 md:mt-0 text-center">
            <span className="text-xs lg:text-sm">{props.storeName}</span>
        </div>
    );
}

const ProductRow = (props: {stores: string[], product: Product}) => {
    let cheapest = Math.min(...props.stores.map(store => props.product.prices[store.toLowerCase()]?.actualPrice ?? Infinity));

    return (
        <div className="group flex justify-center md:justify-end
                        items-center justify-items-center flex-wrap md:flex-nowrap mb-3 md:mb-0 px-3 py-0.5">
            <ProductName name={props.product.name} />
            {
                props.stores.sort().map(store => {
                    let storeName = store.toLowerCase();
                    let price = props.product.prices[storeName];
                    return <ProductPrice key={storeName} price={price} cheapest={price?.actualPrice == cheapest} />;
                })
            }
        </div>
    );
}

const ProductName = (props: {name: string}) => {
    return ( /* transition-colors transition-100 */
        <div className="flex-grow basis-full md:basis-auto cursor-pointer inline-block mr-6
                        text-center md:text-right text-xs lg:text-sm
                        group-hover:text-blue-500 font-semibold">
            {props.name}
        </div>
    );
}

const ProductPrice = (props: {price: Price, cheapest: boolean}) => {
    let color = 'transparent';
    const style = 'inline-block min-w-[3.5em] sm:min-w-[5em] sm:w-[5em] mt-1 ml-1 md:mt-0 py-[1em] lg:py-[0.5em] text-center '

    if (props.price == null) { // store doesn't contain product
        return <div className={style + color}>-</div>;
    }

    switch (props.price.discount) {
        case Discount.None:
            color = 'bg-stone-100'
            break;
        case Discount.Normal:
            color = 'bg-yellow-400';
            break;
        case Discount.Member:
            color = 'bg-orange-400';
    }
    return <div className={style + color + (props.cheapest ? ' font-bold' : '')}>{props.price.actualPrice}</div>;
}

export default ProductList;
