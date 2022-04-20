import React, { ChangeEventHandler, useState } from 'react';


const SearchBar = () => {
    return (
        <div className="flex sm:col-start-2 md:col-start-3 xl:col-start-1 row-start-2
                        col-span-10 sm:col-span-8 md:col-span-6 xl:col-span-3 shadow xl:sticky top-3">
            <SearchInput />
            <SearchButton />
        </div>
    );
}

const SearchInput = () => {
    let [searchText, setSearchText] = useState<string>('');

    return (
        <input type="text" autoComplete="off" name="search" tabIndex={1}
               onChange={e => setSearchText(e.target.value)} value={searchText} placeholder="Otsi tooteid..."
               className="flex-grow appearance-none h-12 px-4 py-2 focus:outline-none border-0
                          bg-stone-50 text-base text-stone-800" />
    );
}

const SearchButton = () => {
    return (
        <div className="flex flex-col h-12 w-12 justify-center bg-blue-500">
            <span className="material-icons select-none cursor-pointer text-center text-neutral-100 text-3xl">
                search
            </span>
        </div>
    );
}

export default SearchBar;
