class PostRoute:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_route = self.request.get_full_path()
        context['current_route'] = current_route
        return context
