from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.mixins import (LoginRequiredMixin,
UserPassesTestMixin)

from django.views.generic import (ListView, DetailView,
        CreateView, UpdateView, DeleteView) 
from .data import *
from django.contrib.auth.models import User
from .models import *
# from django.conf import settings
# User = settings.AUTH_USER_MODEL

# Entire functionality of the site is performed here
f = open('StockCode.json')
data=json.load(f)
CompanyNames=data.keys()

def home(request):
    # making dictionary of all the posts records from the database
    context = {
        'posts': Post.objects.all(),
        'CompanyNames':CompanyNames
    }
    return render(request, 'home.html', context)

class PostListView(ListView):

    def get_context_data(self,*args, **kwargs):
        context = super(PostListView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    
    model = Post
    template_name = 'home.html' # <model>_<viewtype>.html
    context_object_name = 'posts'  
    ordering = ['-date_posted']  
    paginate_by = 5


class UserPostListView(ListView):
    # this class makes list view which shows the posts of particular user 
    
    def get_context_data(self,*args, **kwargs):
        context = super(UserPostListView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    
    model = Post
    template_name = 'user_post.html' # <model>_<viewtype>.html
    context_object_name = 'posts'  
    paginate_by = 5

    # This function takes the clicket username and returns all the posts of that user 
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    # this class is used when we have to see single post at a time 
    
    def get_context_data(self,*args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    # this class creates new form so that user can make post new posts 
    # LoginRequiredMixin helps that user must be login when he wants to add or post
    # fields are used which allocates respective components required to make new post 
    # title will give textfield to enter short title
    # content will give textarea to enter large content 
    model = Post
    fields = ['title', 'content']
    
    def get_context_data(self,*args, **kwargs):
        context = super(PostCreateView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    

    # this function takes form to make new post and validate the form 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # this class is used to update present posts 
    # This functionality also requires login 
    # UserPassesTestMixin uses below mentioned test_func which allows the user to update 
    # which has made that post other wise throw error
    model = Post
    fields = ['title', 'content']
    
    def get_context_data(self,*args, **kwargs):
        context = super(PostUpdateView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return(self.request.user == post.author)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # Similar to update class 
    model = Post
    success_url = '/'
    
    def get_context_data(self,*args, **kwargs):
        context = super(PostDeleteView, self).get_context_data(*args,**kwargs)
        context['CompanyNames'] =CompanyNames
        return context
    
    # whenever successfull execution of function success url will be directed
    def test_func(self):
        post = self.get_object()
        return(self.request.user == post.author)




def NewsFunc(request):
    rNews=RecentNews()
    f = open('StockCode.json')
    data=json.load(f)
    CompanyNames=data.keys()
    context={
        'rNews':rNews,
        'CompanyNames':CompanyNames,
    }

    return render(request,'news.html',context)


def CompanyInformation(request,cmpname):
    f = open('StockCode.json')
    data=json.load(f)
    CompanyNames=data.keys()
    cmpData=fetchCompanyData(cmpname)
    
    available=True
    if isinstance(cmpData, str):
        available=False
        context={
            'CompanyNames':CompanyNames,
            'available':available,
            'cmpData':cmpData
        }
        return render(request,'companyInfo.html',context)
    

    context={
        'CompanyNames':CompanyNames,
        'available':available,
        'cmpData':cmpData,
    }
    return render(request,'companyInfo.html',context)




def companyGraph(request,cmpname=None):
        #for generating the companies arry in javascript
        Array=""
        Index=0
        cnt=0
        for i in data:
            if i==cmpname:
                Index=cnt   
            Array+=f"'BSE:{data[i]}',"
            cnt=cnt+1

        cmpId=data[cmpname]    
        

        code=f'''<div>
        <div class="container">
            <div id="tradingview_6dff5"></div>
            <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/BSE-{cmpId}/" rel="noopener" target="_blank"><span class="blue-text">HDFCBANK Chart</span></a> by TradingView</div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                var companies = [{Array}]
            new TradingView.widget(
            \u007b
            "width": 600,
            "height": 410,
            "symbol": companies[{Index}],
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "in",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "details": true,
            "container_id": "tradingview_6dff5"
        \u007d
            );
            </script>
        </div>
    </div> '''
        quantity=1
        f2="sell" in request.POST
        f1="buy" in request.POST
        if f1 or f2 :
            if f1:
                quantity=int(request.POST.get('quantity'))
                calling(cmpId,quantity,1)
            else:
                quantity=int(request.POST.get('quantity'))
                calling(cmpId,quantity,2)    
        
        context={
            'CompanyNames':CompanyNames,
            'code':code,
            'id':0,
            'quantity':quantity
        }
        return render(request,'home1.html',context)  
    




def portfolio(request):
    if request.method=="POST": 
        
        obj=request.POST.getlist("select")
        cmp_objj={}
        for i in obj:
            cmp_objj[i]=0

        Id=User.objects.filter(username=request.user)[0].id 
        Id1=0  
        if len(dbobj.objects.filter(author_id=Id))==0:
            dbobj=portfolioDb(author_id=Id,compnay=cmp_objj)    
            dbobj.save()
            Id1=1
        else:
              pass

        context={'CompanyNames':CompanyNames}
        return render(request,'portfolio.html',context)
    else:
        print(request.user)
        context={'CompanyNames':CompanyNames}
        return render(request,'portfolio.html',context) 


def Homepage(request):
    Array=""
    for i in data:   
        Array+=f"'BSE:{data[i]}',"
        
    code=f'''<div>
        <div class="container">
            <div id="tradingview_6dff5"></div>
            <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/BSE/" rel="noopener" target="_blank"><span class="blue-text">HDFCBANK Chart</span></a> by TradingView</div>
            <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
            <script type="text/javascript">
                var companies = [{Array}]
            new TradingView.widget(
            \u007b
            "width": 580,
            "height": 410,
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "in",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": false,
            "allow_symbol_change": true,
            "details": true,
            "container_id": "tradingview_6dff5"
        \u007d
            );
            </script>
        </div>
    </div> '''
    context={'CompanyNames':CompanyNames,'code':code}
    return render(request,'home1.html',context)