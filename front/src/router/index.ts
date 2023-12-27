import Index from '../views/index.vue'
import BookList from '../views/booklist.vue'
import SBook from '../views/sbook.vue'
import User from '../views/user.vue'
import Center from '../views/ChildViews/center.vue'
import ChangePwd from '../views/ChildViews/changePwd.vue'
import UserOrder from '../views/ChildViews/userOrder.vue'
import UserAddress from '../views/ChildViews/userAddr.vue'
import Category from '../views/category.vue'
import Carts from '../views/cart.vue'
import Order from '../views/order.vue'
import Success from '@/views/success.vue'
import Search from '@/views/search.vue'
import AllGoods from '@/views/allgoods.vue'
import BuyedBook from '../views/ChildViews/buyedBook.vue'
import SellBook from '../views/ChildViews/sellBook.vue'
import BookOnSale from '../views/ChildViews/bookOnSale.vue'
import BindPhone from '../views/ChildViews/bindPhone.vue'
import Transactions from '../views/ChildViews/transactions.vue'
import Recommend from '@/views/recommend.vue'
import { createRouter,createWebHashHistory,createWebHistory} from "vue-router";

const routes = [
    {   
      path: '/', 
      name: 'index',
      component: Index,
    },
    {
      path:'/book/:id',
      name: 'book',
      component: BookList,
    },
    {
      path:'/sbook/:id',
      name:'sbook',
      component:SBook,
    },
    {
      path:'/user/',
      name:'user',
      component:User,
      children:[{
        path:'center',
        component:Center,
      },{
        path:'changePwd',
        component:ChangePwd,
      },{
        path:'order',
        component:UserOrder,
      },{
        path:'receive_address',
        component:UserAddress,
      },{
        path:'buyedBook',
        component:BuyedBook,
      },{
        path:'sell',
        component:SellBook
      },{
        path:'bookOnSale',
        component:BookOnSale
      },{
        path:'bindPhone',
        component:BindPhone
      },{
        path:'transactions',
        component:Transactions
      }]
    },
    {
      path:'/category',
      name:'category',
      component:Category,
    },
    {
      path:'/cart',
      name:'cart',
      component:Carts,
    },
    {
      path:'/easyBuy',
      name:'easyBuy',
      component:Order,
    },
    {
      path:'/success',
      name:'success',
      component:Success,
    },
    {
      path:'/search',
      name:'search',
      component:Search
    },{
      path:'/all/:id',
      name:'allGoods',
      component:AllGoods
    },{
      path:'/recommend',
      name:'recommend',
      component:Recommend
    }
  ]
  
const router = createRouter({
//   mode:'history',
  history: createWebHistory(),
  routes, // `routes: routes` 的缩写
})

export default(
    router
)
