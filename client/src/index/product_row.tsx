import React from 'react';
import Popup from 'reactjs-popup';

import { Product, Price, Discount } from './index';


const ProductRow = (props: {stores: string[], product: Product, item_layout: string}) => {
    const cheapest = Math.min(...props.stores.map(store => props.product.prices[store.toLowerCase()]?.actualPrice ?? Infinity));

    const row = (
        <div className="group flex justify-center md:justify-end
                        items-center justify-items-center flex-wrap md:flex-nowrap
                        mx-1.5 sm:mx-3 lg:mx-5 mb-2 md:mb-1 py-0.5 pb-2 md:pb-1
                        border-0 border-b-[1px] border-neutral-200">
            <ProductName name={props.product.name} />
            {
                props.stores.sort().map(store => {
                    let storeName = store.toLowerCase();
                    let price = props.product.prices[storeName];
                    let is_cheapest = price?.actualPrice == cheapest;
                    return <ProductPrice key={storeName} price={price} cheapest={is_cheapest} item_layout={props.item_layout} />;
                })
            }
        </div>
    );

    return (
        <Popup trigger={row} modal>
            {(onClose: () => void) => (
                <ProductDetail onClose={onClose} product={props.product} />
            )}
        </Popup>
    );
}

const ProductDetail = (props: {onClose: () => void, product: Product}) => {
    return (
        <div className="shadow-xl border m-10 bg-stone-50 font-main text-neutral-800">
            <div className="flex justify-between items-center">
                <span className="material-icons material-icon m-1.5 text-left text-neutral-600 text-3xl leading-none">close</span>
                <span className="flex-grow text-center pl-10 pr-5 py-3 font-semibold">{props.product.name}</span>
            </div>

            <div className="flex flex-col justify-center items-center px-10 py-5">
                <p>{props.product.id}</p>
                <p>{'text '.repeat(100)}</p>
            </div>
        </div>
    );
}

const ProductName = (props: {name: string}) => {
    return (
        <div className="flex-grow basis-full md:basis-auto cursor-pointer inline-block md:mr-6
                        text-center md:text-right text-xs lg:text-sm
                        group-hover:text-blue-500 font-semibold">
            {props.name}
        </div>
    );
}

const ProductPrice = (props: {price: Price, cheapest: boolean, item_layout: string}) => {
    let color = 'transparent';
    const priceStyle = ['py-2', props.item_layout].join(' ');

    if (props.price == null) { // store doesn't contain product
        return <div className={[priceStyle, props.item_layout, color].join(' ')}>-</div>;
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
    return (
        <div className={[priceStyle, color, props.cheapest ? 'font-bold' : ''].join(' ')}>
            {props.price.actualPrice}
        </div>
    );
}

export default ProductRow;
