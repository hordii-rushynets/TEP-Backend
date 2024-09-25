from rest_framework import serializers

from tep_user.models import TEPUserSocialNetworks

from .models import Post, Tag, Complexity, Requirements, Materials, ForChildren


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title_uk', 'title_en', 'title_ru']


class ComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Complexity
        fields = ('id', 'photo', 'title_uk', 'title_en', 'title_ru', 'description_uk',
                  'description_en', 'description_ru', 'post')


class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ('id', 'title_uk', 'title_en', 'title_ru', 'description_uk',
                  'description_en', 'description_ru', 'post')


class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materials
        fields = ('id', 'photo', 'title_uk', 'title_en', 'title_ru', 'description_uk', 'description_en',
                  'description_ru', 'post')


class ForChildrenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForChildren
        fields = ('id', 'photo', 'description_uk', 'description_en', 'description_ru',
                  'additional_description_uk', 'additional_description_en', 'additional_description_ru', 'post')


class PostSerializer(serializers.ModelSerializer):
    tags = TagTitleSerializer(read_only=True, many=True)
    author = serializers.SerializerMethodField()
    complexity = ComplexitySerializer(read_only=True)
    requirements = RequirementsSerializer(read_only=True)
    what_materials = MaterialsSerializer(read_only=True)
    for_children = ForChildrenSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title_uk', 'title_en', 'title_ru', 'meta_description_uk', 'meta_description_en',
                  'meta_description_ru', 'slug', 'image', 'created_at', 'author', 'complexity', 'requirements',
                  'what_materials', 'for_children', 'tags')

    def get_author(self, post: Post) -> dict:
        """Method to retrieve an infromation about social networks of post author."""
        social_networks = TEPUserSocialNetworks.objects.filter(user=post.author)

        author = {
            'name': post.author.full_name,
            'social_networks': {}
        }

        for social_network in social_networks:
            author['social_networks'][social_network.types] = social_network.url

        return author
