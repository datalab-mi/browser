import { readable, writable, derived } from 'svelte/store';

// auth: https://www.toptal.com/front-end/svelte-framework-guide
export const itemConfig = writable({})
export const searchList = writable([[]])
export const promiseSearch = writable(new Promise(()=>{}))

export const suggestEntry = writable([]);

export const isReindex = writable(false)

export const list_synonym = writable([])
export const list_files = writable([])


// authentification
const initial_user = {role:"common", jwToken:null}

async function testToken(user, set) {
  const response = await fetch('/api/admin/identity', {
    headers: new Headers({'Authorization': `JWT ${user.jwToken}`})
  });
  console.log(response)
  if(response.ok) {
    set(user)
  }
  else if (response.status === 401) {
    set(initial_user)
  }
}

function createUser(user) {
  const { subscribe, set, update } = writable(user, () => testToken(user, set))
  console.log('got a user');
  return {
    subscribe,
    authenticate: (user) => {
      set(user)
      localStorage.setItem('user', JSON.stringify(user))
    },
    clean: () => localStorage.removeItem('user'),
    updateKey: (key, value) => {
      update(user => user.key = value)
    }

  };
}

export let user
if(typeof window !== "undefined") {
    user = createUser(JSON.parse(localStorage.getItem("user")) || initial_user);
} else {
    user = createUser(initial_user);
}

export const displayLogin = writable(false)
export const headers = derived(user,  $user => {Authorization: `JWT ${$user.jwToken}`})
// logger
const inital_logger_list = [{level: "error",message: "erreur grave", ressource: "authentification", status:401},
        {level: "info",message: "document telechargé", ressource: "upload", status:200}]

// custom store for the logger, every 10 seconds lost first element (the oldest)
function createLogger() {
	const { subscribe, set, update } = writable([], () => {
	console.log('got a subscriber');
	const interval = setInterval(() => {
		update(n => n.slice(1, n.length))
	}, 10000);	return () => console.log('no more subscribers');
});

	return {
		subscribe,
		concat: (x) => update(n => n.concat(x)),
		filter: (msg, key) => update(n => n.filter(t => t[key] !== msg)),
    delete: () => update(n => n.slice(1, n.length)),
		reset: () => set(inital_logger_list)
	};
}

export const list_logger = createLogger();


async function fetchUserData(set) {
  console.log("fetchUserData")
  const res = await fetch('user/env.json');
  if(res.ok) {
    const data_res = await res.json();
    console.log(data_res);
    set(data_res);
  } else {
    const text = res.text();
    throw new Error(text);
  }
}

function getUserData() {
  const { subscribe, set, update } = writable({}, () => fetchUserData(set));
  console.log('got a data');

  return  { subscribe }
}
export const userData = getUserData();
