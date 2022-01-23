from rest_framework import serializers

from posts.models import Comment, Group, Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CreateOnlyDefault('')
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    group = serializers.StringRelatedField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)

        if 'group' in self.initial_data:
            group = self.initial_data['group']
            post.group = Group.objects.get(pk=group)
            post.save()

        return post

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)

        if 'group' in self.initial_data:
            group = self.initial_data['group']
            instance.group = Group.objects.get(pk=group)

        instance.save()
        return instance
