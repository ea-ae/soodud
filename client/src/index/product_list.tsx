import React from 'react';


interface Product {
    name: string
    prices: Prices
}

interface Prices {
    [key: string]: Price
}

interface Price {
    basePrice?: number
    actualPrice: number
    discount: Discount
}

enum Discount {
    None = 'NONE',
    Normal = 'NORMAL',
    Member = 'MEMBER'
}

const ProductList = () => {
    const stores = ['Coop', 'Maxima', 'Prisma', 'Rimi', 'Selver'];
    const product: Product = {
        name: 'Sample product',
        prices: {
            rimi: {actualPrice: 14.99, discount: Discount.None},
            maxima: {actualPrice: 3.99, discount: Discount.Normal},
            prisma: {actualPrice: 5.99, discount: Discount.None},
            coop: {actualPrice: 4.99, discount: Discount.Member},
        }
    };

    return (
        <div className="row-start-3 xl:row-start-auto xl:row-span-3 col-span-10 xl:col-span-7 bg-transparent text-stone-800">
        <div className="shadow-sm cursor-default py-2 px-1 lg:px-5 bg-stone-50 text-sm lg:text-base">
            <ProductListHeader stores={stores} />
            <ProductRow stores={stores} product={product} />
        </div>
    </div>
    );
}

const ProductListHeader = (props: {stores: string[]}) => {
    return (
        <div className="group flex justify-center md:justify-end items-center justify-items-center
                        flex-wrap md:flex-nowrap px-2 text-stone-600">
            {props.stores.sort().map(store => <ProductListHeaderStore storeName={store} />)}
        </div>
    );
}

const ProductListHeaderStore = (props: {storeName: string}) => {
    return (
        <div className="inline-block min-w-[5em] mt-1 md:mt-0 ml-1 text-center">
            <span className="text-xs lg:text-sm">{props.storeName}</span>
        </div>
    );
}

const ProductRow = (props: {stores: string[], product: Product}) => {
    let cheapest = Math.min(...props.stores.map(store => props.product.prices[store.toLowerCase()]?.actualPrice ?? Infinity));
    console.log(`cheapest is ${cheapest}`);

    return (
        <div className="group flex justify-center md:justify-end
                        items-center justify-items-center flex-wrap md:flex-nowrap px-2 py-1">
            <ProductName name={props.product.name} />
            {
                props.stores.sort().map(store => {
                    let price = props.product.prices[store.toLowerCase()];
                    return <ProductPrice price={price} cheapest={price?.actualPrice == cheapest} />;
                })
            }
        </div>
    );
}

const ProductName = (props: {name: string}) => {
    return (
        <div className="flex-grow basis-full md:basis-auto inline-block mr-6
                        text-center md:text-right text-xs lg:text-sm
                        group-hover:text-blue-500 transition-colors font-semibold">
            {props.name}
        </div>
    );
}

const ProductPrice = (props: {price: Price, cheapest: boolean}) => {
    let color = 'transparent';
    const style = 'inline-block min-w-[5em] mt-1 md:mt-0 ml-1 py-[1em] lg:py-[0.5em] text-center bg-'

    if (props.price == null) { // store doesn't contain product
        return <div className={style + color}>-</div>;
    }

    switch (props.price.discount) {
        case Discount.Normal:
            color = 'yellow-400';
            break;
        case Discount.Member:
            color = 'amber-500';
    }
    return <div className={style + color + (props.cheapest ? ' font-bold' : '')}>{props.price.actualPrice}</div>;
}

export default ProductList;
